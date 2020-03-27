"""Represents a batch pickup response message."""

from marshmallow import fields
from typing import Sequence

from ....messaging.agent_message import AgentMessage, AgentMessageSchema
from .inner.pickup_message_inner import PickupMessageInner, PickupMessageInnerSchema
from ..message_types import BATCH_PICKUP_RESPONSE, PROTOCOL_PACKAGE


HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers."
    "batch_pickup_response_handler.BatchPickupResponseHandler"
)


class BatchPickupResponse(AgentMessage):
    """Class representing a batch pickup response."""

    class Meta:
        """Metadata for a batch pickup response."""

        handler_class = HANDLER_CLASS
        schema_class = "BatchPickupResponseSchema"
        message_type = BATCH_PICKUP_RESPONSE

    def __init__(
        self,
        messages_attach: Sequence[PickupMessageInner] = None,
        **kwargs
    ):
        """
        Initialize batch pickup response object.

        Args:
            messages_attach: Message details object

        """
        super(BatchPickupResponse, self).__init__(**kwargs)
        self.messages_attach = (
            list(messages_attach) if messages_attach else []
        )


class BatchPickupResponseSchema(AgentMessageSchema):
    """Batch pickup response schema class."""

    class Meta:
        """Batch pickup response schema metadata."""

        model_class = BatchPickupResponse

    messages_attach = fields.Nested(
        PickupMessageInnerSchema,
        required=True,
        many=True,
        data_key="messages~attach",
    )
