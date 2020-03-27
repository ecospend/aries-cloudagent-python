"""List pickup request content message."""

from marshmallow import fields
from typing import Sequence

from ....messaging.agent_message import AgentMessage, AgentMessageSchema
from ..message_types import LIST_PICKUP_REQUEST, PROTOCOL_PACKAGE

HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers"
    ".list_pickup_handler.ListPickupHandler"
)


class ListPickupRequest(AgentMessage):
    """Class representing a list pickup request."""

    class Meta:
        """Metadata for a list pickup request."""

        handler_class = HANDLER_CLASS
        message_type = LIST_PICKUP_REQUEST
        schema_class = "ListPickupRequestSchema"

    def __init__(
        self,
        *,
        message_ids: Sequence[str] = None,
        **kwargs,
    ):
        """
        Initialize list pickup request object.

        Args:
            message_ids: List of pickup message identity
        """
        super(ListPickupRequest, self).__init__(**kwargs)
        self.message_ids = list(message_ids) if message_ids else None


class ListPickupRequestSchema(AgentMessageSchema):
    """List pickup request schema class."""

    class Meta:
        """List pickup request schema metadata."""

        model_class = ListPickupRequest

    message_ids = fields.List(
        fields.Str(description="Message identity"),
        data_key="message_ids",
        required=True,
        description="List of message identities",
    )
