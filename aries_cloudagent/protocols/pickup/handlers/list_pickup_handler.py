"""List pickup request handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.list_pickup_request import ListPickupRequest
from ..manager import PickupManager


class ListPickupHandler(BaseHandler):
    """Request handler for list pickup requests."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for list pickup request.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("ListPickupHandler called with context %s", context)
        assert isinstance(context.message, ListPickupRequest)
        self._logger.info(
            "Received list pickup request message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException("No connection established for list pickup request")

        pickup_manager = PickupManager(context)
        response = await pickup_manager.receive_list_request()
        await responder.send_reply(response)
