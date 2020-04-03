"""Status response handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.status_response import StatusResponse


class StatusResponseHandler(BaseHandler):
    """Response handler for status responses."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for status response.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("StatusResponseHandler called with context %s", context)
        assert isinstance(context.message, StatusResponse)
        self._logger.info(
            "Received status response message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException(
                "No connection established for status response"
                )
