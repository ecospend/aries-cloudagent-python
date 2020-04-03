"""Status of pickup messages."""

from ....messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import STATUS_REQUEST, PROTOCOL_PACKAGE

HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers.status_request_handler.StatusRequestHandler"
)


class StatusRequest(AgentMessage):
    """Class representing pickup message status."""

    class Meta:
        """Pickup message status metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "StatusRequestSchema"
        message_type = STATUS_REQUEST

    def __init__(self, *, issue: str = None, **kwargs):
        """Initialize status request object."""
        super(StatusRequest, self).__init__(**kwargs)


class StatusRequestSchema(AgentMessageSchema):
    """Status request schema."""

    class Meta:
        """Status request schema metadata."""

        model_class = StatusRequest
