"""Delete response of pickup messages."""

from marshmallow import fields
from typing import Sequence

from ....messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import DELETE_PICKUP_RESPONSE, PROTOCOL_PACKAGE

HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers.delete_pickup_response_handler.DeletePickupResponseHandler"
)


class DeletePickupResponse(AgentMessage):
    """Class representing pickup message delete response."""

    class Meta:
        """Pickup message delete metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "DeletePickupResponseSchema"
        message_type = DELETE_PICKUP_RESPONSE

    def __init__(
        self,
        *,
        message_ids : Sequence[str] = None,
        **kwargs
        ):
        """Initialize pickup delete response object."""
        super(DeletePickupResponse, self).__init__(**kwargs)
        self.message_ids = list(message_ids) if message_ids else None


class DeletePickupResponseSchema(AgentMessageSchema):
    """Pickup delete response schema."""

    class Meta:
        """Pickup delete response schema metadata."""

        model_class = DeletePickupResponse

    message_ids = fields.List(
        fields.Str(description="Message identity"),
        data_key="message_ids",
        required=True,
        description="List of message identities to delete",
    )