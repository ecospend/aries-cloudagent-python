"""List pickup response handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.list_pickup_response import ListPickupResponse


class ListPickupResponseHandler(BaseHandler):
    """Response handler for list pickup responses."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for list pickup response.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("ListPickupResponseHandler called with context %s", context)
        assert isinstance(context.message, ListPickupResponse)
        self._logger.info(
            "Received list pickup response message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException(
                "No connection established for list pickup response"
                )
