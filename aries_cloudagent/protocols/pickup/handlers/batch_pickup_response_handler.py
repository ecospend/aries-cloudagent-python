"""Batch pickup response handler."""

from ....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext
)

from ..messages.batch_pickup_response import BatchPickupResponse


class BatchPickupResponseHandler(BaseHandler):
    """Response handler for batch pickup responses."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for batch pickup response.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("BatchPickupResponseHandler called with context %s", context)
        assert isinstance(context.message, BatchPickupResponse)
        self._logger.info(
            "Received batch pickup response message: %s",
            context.message.serialize(as_string=True)
        )

        if not context.connection_ready:
            raise HandlerException(
                "No connection established for batch pickup response"
                )
