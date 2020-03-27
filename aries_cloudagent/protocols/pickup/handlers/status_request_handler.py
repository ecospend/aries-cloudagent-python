"""Status of pickup message handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext,
)

from ..messages.status_request import StatusRequest
from ..manager import PickupManager


class StatusRequestHandler(BaseHandler):
    """Message handler class for status."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Status handler logic for batch pickup request.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"StatusRequestHandler called with context {context}")
        assert isinstance(context.message, StatusRequest)

        if not context.connection_ready:
            raise HandlerException("No connection established for status request")

        pickup_manager = PickupManager(context)
        response = await pickup_manager.receive_status_request()
        await responder.send_reply(response)
