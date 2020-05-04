"""Handle pickup message information."""

from marshmallow import fields

from ....config.injection_context import InjectionContext
from ....messaging.models.base_record import BaseRecord, BaseRecordSchema

from aries_cloudagent.messaging.valid import UUIDFour


class PickupMessage(BaseRecord):
    """Represents an Valido Pickup Message."""

    class Meta:
        """PickupMessage metadata."""

        schema_class = "PickupMessageSchema"

    RECORD_TYPE = "pickup_message"
    RECORD_ID_NAME = "message_id"
    WEBHOOK_TOPIC = "pickup_message"
    LOG_STATE_FLAG = "debug.pickup_message"
    TAG_NAMES = {
        "verkey"
        }

    INITIATOR_SELF = "self"
    INITIATOR_EXTERNAL = "external"

    STATE_MESSAGE_WAIT = "message_wait"
    STATE_MESSAGE_SENT = "message_sent"
    STATE_MESSAGE_RECEIVED = "message_received"

    def __init__(
        self,
        *,
        message_id: str = None,
        target_url: str = None,
        verkey: str = None,
        message: dict = None,
        state: str = STATE_MESSAGE_WAIT,
        **kwargs
    ):
        """Initialize a new StoredMessage."""
        super().__init__(message_id, state, **kwargs)
        self.state = state
        self.target_url = target_url
        self.verkey = verkey
        self.message = message

    @property
    def message_id(self) -> str:
        """Accessor for the ID associated with this message."""
        return self._id

    @property
    def message_query(self) -> str:
        """Accessor for the ID associated with this message."""
        return self._id

    @property
    def record_value(self) -> dict:
        """Accessor for JSON record value generated for this presentation exchange."""
        return {
            prop: getattr(self, prop)
            for prop in (
                "target_url",
                "verkey",
                "message",
                "state"
            )
        }

    @classmethod
    async def retrieve_by_verkey(
        cls, context: InjectionContext, verkey: str
    ) -> "PickupMessage":
        """Retrieve pickup messages by verkey."""

        tag_filter = {}
        tag_filter["verkey"] = verkey
        post_filter = {}

        records = await PickupMessage.query(context, tag_filter, post_filter)

        return records

    async def set_delivered(
        self, context: InjectionContext
    ):
        """Set message status to delivered."""

        self.state = PickupMessage.STATE_MESSAGE_SENT
        await self.save(context=context)

class PickupMessageSchema(BaseRecordSchema):
    """Schema to allow serialization/deserialization of pickup messages."""

    class Meta:
        """PickupMessageSchema metadata."""

        model_class = PickupMessage

    message_id = fields.Str(
        required=True,
        description="Unique message identifier",
        example=UUIDFour.EXAMPLE,
    )
    target_url = fields.Str(
        required=False,
        description="Receipent target url",
        example=UUIDFour.EXAMPLE,  # typically a UUID4 but not necessarily
    )
    verkey = fields.Str(
        required=False,
        description="Receipent Verkey",
        example="6e59KeK6bucRQP2qzJkdLthb2dL5jEyQx5G9Dc5CatK2",
    )
    message = fields.Dict(
        required=False,
        description="Stored message",
        example="content:Hello",
    )
