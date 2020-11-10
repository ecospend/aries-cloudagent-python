"""Delete request of pickup messages."""

from ....messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import DELETE_PICKUP_REQUEST, PROTOCOL_PACKAGE

HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers.delete_pickup_handler.DeletePickupHandler"
)


class DeletePickupRequest(AgentMessage):
    """Class representing pickup message delete request."""

    class Meta:
        """Pickup message delete metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "DeletePickupRequestSchema"
        message_type = DELETE_PICKUP_REQUEST

    def __init__(
        self,
        *,
        message_ids = Sequence[str] = None,
        **kwargs
        ):
        """Initialize pickup delete request object."""
        super(DeletePickupRequest, self).__init__(**kwargs)
        self.message_ids = list(message_ids) if message_ids else None


class DeletePickupRequestSchema(AgentMessageSchema):
    """Pickup delete request schema."""

    class Meta:
        """Pickup delete request schema metadata."""

        model_class = DeletePickupRequest

    message_ids = fields.List(
        fields.Str(description="Message identity"),
        data_key="message_ids",
        required=True,
        description="List of message identities to delete",
    )