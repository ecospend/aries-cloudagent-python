"""Batch pickup request handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.batch_pickup_request import BatchPickupRequest
from ..manager import PickupManager


class BatchPickupHandler(BaseHandler):
    """Request handler for batch pickup requests."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for batch pickup request.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("BatchPickupHandler called with context %s", context)
        assert isinstance(context.message, BatchPickupRequest)
        self._logger.info(
            "Received batch pickup request message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException("No connection established for batch pickup request")

        pickup_manager = PickupManager(context)
        response, pickup_messages = await pickup_manager.receive_pickup_request()
        await responder.send_reply(response)
        for message in pickup_messages :
            await message.set_delivered(context=context)
