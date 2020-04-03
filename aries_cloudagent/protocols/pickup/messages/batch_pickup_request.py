"""A batch pickup request content message."""

from marshmallow import fields

from ....messaging.agent_message import AgentMessage, AgentMessageSchema
from ..message_types import BATCH_PICKUP_REQUEST, PROTOCOL_PACKAGE

HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers"
    ".batch_pickup_handler.BatchPickupHandler"
)


class BatchPickupRequest(AgentMessage):
    """Class representing a batch pickup request."""

    class Meta:
        """Metadata for a batch pickup request."""

        handler_class = HANDLER_CLASS
        message_type = BATCH_PICKUP_REQUEST
        schema_class = "BatchPickupRequestSchema"

    def __init__(
        self,
        *,
        batch_size: int = None,
        **kwargs,
    ):
        """
        Initialize batch pickup request object.

        Args:
            batch_size: Count of messages to be sent to the recipient
        """
        super(BatchPickupRequest, self).__init__(**kwargs)
        self.batch_size = batch_size


class BatchPickupRequestSchema(AgentMessageSchema):
    """Batch pickup request schema class."""

    class Meta:
        """Batch pickup request schema metadata."""

        model_class = BatchPickupRequest

    batch_size = fields.Int(
        required=False,
        description="Count of messages to be sent to the recipient",
    )
