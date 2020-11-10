"""Delete pickup response handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.delete_pickup_response import DeletePickupResponse
from ..manager import PickupManager


class DeletePickupResponseHandler(BaseHandler):
    """Request handler for delete pickup response."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for delete pickup response.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("DeletePickupResponseHandler called with context %s", context)
        assert isinstance(context.message, DeletePickupResponse)
        self._logger.info(
            "Received delete pickup response message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException("No connection established for list pickup request")

        pickup_manager = PickupManager(context)
        response, pickup_messages = await pickup_manager.receive_delete_pickup_response()