"""Push notification outbound transport."""

import logging
import json
from typing import Union
from pyfcm import FCMNotification
from urllib.parse import urlparse


from ...config.injection_context import InjectionContext

from ..stats import StatsTracer

from .base import BaseOutboundTransport, OutboundTransportError


class PushTransport(BaseOutboundTransport):
    """Push notification outbound transport class."""

    schemes = ("push")

    def __init__(self) -> None:
        """Initialize an `PushTransport` instance."""
        super(PushTransport, self).__init__()
        self.push_service = None
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

        if not self.push_service:
            self.push_key = context.settings.get(
                "transport.push_api_key"
                )
            self.push_service = FCMNotification(api_key=self.push_key)

        endpoint_args = urlparse(endpoint)
        push_id = endpoint_args.netloc

        payload_size = len(payload)

        if(payload_size < 3500):
            label = context.settings.get(
                "default_label"
                )
            agent_message = {
                "Data": {
                            "type": "agent_message",
                            "message": json.loads(payload),
                            "message_type": "direct"
                },
                "Aps": {
                    "alert": "You have new message from {}".format(label),
                    "sound": "default",
                    "badge": 0,
                    "title": "{}".format(label)
                }
            }
            result = self.push_service.notify_single_device(
                registration_id=push_id,
                data_message=agent_message
            )
            if result['success'] < 1:
                raise OutboundTransportError("Push message couldn't be delivered")
        else:
            raise OutboundTransportError("Data size exceed push notification limits")
