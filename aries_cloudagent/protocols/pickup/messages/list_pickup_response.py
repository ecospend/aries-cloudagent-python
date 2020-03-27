"""Represents a list pickup response message."""

from marshmallow import fields
from typing import Sequence

from ....messaging.agent_message import AgentMessage, AgentMessageSchema
from .inner.pickup_message_inner import PickupMessageInner, PickupMessageInnerSchema
from ..message_types import LIST_PICKUP_RESPONSE, PROTOCOL_PACKAGE


HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers."
    "list_pickup_response_handler.ListPickupResponseHandler"
)


class ListPickupResponse(AgentMessage):
    """Class representing a list pickup response."""

    class Meta:
        """Metadata for a list pickup response."""

        handler_class = HANDLER_CLASS
        schema_class = "ListPickupResponseSchema"
        message_type = LIST_PICKUP_RESPONSE

    def __init__(
        self,
        messages_attach: Sequence[PickupMessageInner] = None,
        **kwargs
    ):
        """
        Initialize list pickup response object.

        Args:
            messages_attach: Message details object

        """
        super(ListPickupResponse, self).__init__(**kwargs)
        self.messages_attach = (
            list(messages_attach) if messages_attach else []
        )


class ListPickupResponseSchema(AgentMessageSchema):
    """List pickup response schema class."""

    class Meta:
        """List pickup response schema metadata."""

        model_class = ListPickupResponse

    messages_attach = fields.Nested(
        PickupMessageInnerSchema,
        required=True,
        many=True,
        data_key="messages~attach",
    )
