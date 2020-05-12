"""Push notification outbound transport."""

import logging
import firebase_admin
from firebase_admin import messaging
from firebase_admin.exceptions import InvalidArgumentError, FirebaseError
from typing import Union
from urllib.parse import urlparse


from ...config.injection_context import InjectionContext

from ..stats import StatsTracer

from .base import BaseOutboundTransport, OutboundTransportError, PushDataSizeExceedError


class PushTransport(BaseOutboundTransport):
    """Push notification outbound transport class."""

    schemes = ("push")

    def __init__(self) -> None:
        """Initialize an `PushTransport` instance."""
        super(PushTransport, self).__init__()
        firebase_admin.initialize_app()
        self.dry_run = False
        self.apns_config = messaging.APNSConfig(
            headers={
                "apns-priority": "10",
                "apns-push-type": "background"
            },
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    content_available=True
                )
            )
        )
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Start the transport."""
        session_args = {}
        if self.collector:
            session_args["trace_configs"] = [
                StatsTracer(self.collector, "outbound-push:")
            ]
        return self

    async def stop(self):
        """Stop the transport."""
        self.push_service = None

    async def handle_message(
        self, context: InjectionContext, payload: Union[str, bytes], endpoint: str
    ):
        """
        Handle message from queue.

        Args:
            context: the context that produced the message
            payload: message payload in string or byte format
            endpoint: URI endpoint for delivery
        """

        endpoint_args = urlparse(endpoint)
        push_id = endpoint_args.netloc

        payload_size = len(payload)
        if(payload_size < 3500):
            data_message = {
                            "type": "agent_message",
                            "agent_message_type": "direct",
                            "message": payload.decode('utf-8')
            }
            agent_message = messaging.Message(
                data=data_message,
                apns=self.apns_config,
                token=push_id,
                notification=messaging.Notification(
                    body="You've received new message"
                )
            )
            try:
                result = messaging.send(message=agent_message, dry_run=self.dry_run)
            except InvalidArgumentError:
                raise OutboundTransportError("Push message couldn't be delivered")
            except FirebaseError as firebase_error:
                raise OutboundTransportError(str(firebase_error))
            except Exception as api_error:
                raise OutboundTransportError(str(api_error))
            if not result:
                raise OutboundTransportError("Push message couldn't be delivered")
        else:
            raise PushDataSizeExceedError("Data size exceed push notification limits")
