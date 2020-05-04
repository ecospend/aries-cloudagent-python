"""Classes to manage pickup messages."""

import logging
import json
from typing import Sequence

from ...config.injection_context import InjectionContext
from ...core.error import BaseError
from ...messaging.responder import BaseResponder

from .models.pickup_message import PickupMessage

from .messages.batch_pickup_request import BatchPickupRequest
from .messages.batch_pickup_response import BatchPickupResponse

from .messages.inner.pickup_message_inner import PickupMessageInner

from .messages.status_request import StatusRequest
from .messages.status_response import StatusResponse

from .messages.list_pickup_request import ListPickupRequest
from .messages.list_pickup_response import ListPickupResponse

from ...storage.error import StorageNotFoundError


class PickupManagerError(BaseError):
    """Pickup error."""


class PickupManager:
    """Class for managing pickups."""

    def __init__(self, context: InjectionContext):
        """
        Initialize a PickupManager.

        Args:
            context: The context for this message
        """
        self._context = context
        self._logger = logging.getLogger(__name__)

    @property
    def context(self) -> InjectionContext:
        """
        Accessor for the current request context.

        Returns:
            The injection context for this pickup manager

        """
        return self._context

    async def store_pickup_message(
        self,
        message: dict,
        verkey: str,
        target_did: str = None,
        endpoint: str = None
    ):
        """
        Create a pickup message and stores into the wallet.

        Args:
            message: pickup message
            verkey: recipient verkey for stored message
            target_did: did of the recipient

        Returns:
            Stored message id

        """

        stored_message = PickupMessage(verkey=verkey, message=message)
        await stored_message.save(context=self.context)

        if target_did:
            responder: BaseResponder = await self._context.inject(
                    BaseResponder, required=False
                )

            await responder.send_webhook(
                "pickup_message",
                {
                    "target_did": target_did,
                    "message_id": stored_message.message_id,
                    "content": "message_stored",
                    "state": "stored",
                    "endpoint": endpoint
                },
            )

        return stored_message

    async def get_pickup_message(
        self,
        message_id: str
    ):
        """
        Get a single stored pickup message.

        Args:
            message_id: pickup message idetifier

        Returns:
            Pickup message

        """

        pickup_message = await PickupMessage.retrieve_by_id(self.context, message_id)
        return pickup_message

    async def get_pickup_message_list(
        self,
        verkey: str
    ):
        """
        Get a stored pickup messages by verkey or all list.

        Args:
            verkey: recipient verkey for stored messages

        Returns:
            Pickup message list

        """

        records = await PickupMessage.retrieve_by_verkey(self.context, verkey)

        return records

    async def create_pickup_request(
        self,
        batch_size: int,
        connection_id: str
    ):
        """
        Create a batch pickup request.

        Args:
            batch_size: Batch size of pickup messages to send
            connection_id: Connection id for query batch messages

        """
        request = await self.create_pickup_request_object(batch_size=batch_size)
        responder: BaseResponder = await self._context.inject(
                BaseResponder, required=False
            )
        if responder:
            await responder.send(request, connection_id=connection_id)

        return batch_size

    async def create_pickup_request_object(
        self,
        batch_size: int,
    ) -> BatchPickupRequest:
        """
        Create a new batch pickup request.

        Args:
            batch_size: Batch size of pickup messages to send

        Returns:
            A new `BatchPickupRequest` message to send to the other agent

        """

        request = BatchPickupRequest(
           batch_size=batch_size
        )
        return request

    def pickup_message_sort(self, message):
        """Get the sorting key for a particular pickup message."""
        return message["created_at"]

    async def receive_pickup_request(
        self
    ) -> BatchPickupResponse:
        """
        Receive a batch pickup request.

        Returns:
            As batch size pickup messages

        """

        batch_pickup_request: BatchPickupRequest = self.context.message
        verkey = self.context.message_receipt.sender_verkey

        records = await PickupMessage.retrieve_by_verkey(self.context, verkey)

        results = [record.serialize() for record in records]

        results.sort(key=self.pickup_message_sort)

        if len(results) > batch_pickup_request.batch_size:
            results = results[:batch_pickup_request.batch_size]
        response = BatchPickupResponse()
        for stored_message in results:
            pickup_message = PickupMessageInner(
                id=stored_message.get('message_id'),
                message=json.dumps(stored_message.get('message'))
            )
            response.messages_attach.append(pickup_message)
        return response, records

    async def create_status_request(
        self,
        connection_id: str
    ):
        """
        Create a status request.

        Args:
            connection_id: Connection id for query batch messages

        """
        request = await self.create_status_request_object()
        responder: BaseResponder = await self._context.inject(
                BaseResponder, required=False
            )
        if responder:
            await responder.send(request, connection_id=connection_id)

    async def create_status_request_object(
        self,
    ) -> StatusRequest:
        """
        Create a status request.

        Returns:
            A new `StatusRequest` message to send to the other agent

        """

        request = StatusRequest()
        return request

    async def receive_status_request(
        self
    ) -> StatusResponse:
        """
        Receive a status request.

        Returns:
            Batch pickup messages status

        """

        verkey = self.context.message_receipt.sender_verkey
        records = await PickupMessage.retrieve_by_verkey(self.context, verkey)

        undelivered_records = [rec for rec in records if rec.state == PickupMessage.STATE_MESSAGE_WAIT]

        response = StatusResponse()
        response.message_count = len(undelivered_records)
        response.total_size = len(records)

        return response

    async def create_list_request(
        self,
        message_id_list: Sequence[str],
        connection_id: str
    ):
        """
        Create list pickup request.

        Args:
            message_id_list: List of pickup message identity

        """
        request = await self.create_list_request_object(message_id_list=message_id_list)
        responder: BaseResponder = await self._context.inject(
                BaseResponder, required=False
            )
        if responder:
            await responder.send(request, connection_id=connection_id)

        return message_id_list

    async def create_list_request_object(
        self,
        message_id_list: Sequence[str]
    ) -> ListPickupRequest:
        """
        Create a new list pickup request.

        Args:
            message_id_list: List of pickup message identity

        Returns:
            A new `ListPickupRequest` message to send to the other agent

        """

        request = ListPickupRequest(
           message_ids=message_id_list
        )
        return request

    async def receive_list_request(
        self
    ) -> ListPickupResponse:
        """
        Receive a list pickup request.

        Returns:
            List of pickup messages

        """

        list_pickup_request: ListPickupRequest = self.context.message

        response = ListPickupResponse()

        verkey = self.context.message_receipt.sender_verkey
        messages = []

        for message_id in list_pickup_request.message_ids:
            try:
                record = await PickupMessage.retrieve_by_id(self.context, message_id)
            except StorageNotFoundError:
                record = None
            if record and record.verkey == verkey:
                stored_message = record.serialize()
                messages.append(record)
                pickup_message = PickupMessageInner(
                    id=stored_message.get('message_id'),
                    message=json.dumps(stored_message.get('message'))
                )
                response.messages_attach.append(pickup_message)

        return response, messages
