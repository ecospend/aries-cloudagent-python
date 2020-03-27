"""Represents a status response message."""

from marshmallow import fields

from ....messaging.agent_message import AgentMessage, AgentMessageSchema
from ..message_types import STATUS_RESPONSE, PROTOCOL_PACKAGE


HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers."
    "status_response_handler.StatusResponseHandler"
)


class StatusResponse(AgentMessage):
    """Class representing pickup messages status response."""

    class Meta:
        """Metadata for pickup messages status response."""

        handler_class = HANDLER_CLASS
        schema_class = "StatusResponseSchema"
        message_type = STATUS_RESPONSE

    def __init__(
        self,
        message_count: int = None,
        **kwargs
    ):
        """
        Initialize status response object.

        Args:
            message_count: Pickup messages count

        """
        super(StatusResponse, self).__init__(**kwargs)
        self.message_count = message_count


class StatusResponseSchema(AgentMessageSchema):
    """Status response schema class."""

    class Meta:
        """Status response schema metadata."""

        model_class = StatusResponse

    message_count = fields.Int(required=True)
