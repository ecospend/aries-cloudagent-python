"""Batch pickup response's inner message object."""

from marshmallow import fields

from .....messaging.models.base import BaseModel, BaseModelSchema


class PickupMessageInner(BaseModel):
    """Class representing a inner pickup message."""

    class Meta:
        """Inner pickup message metadata."""

        schema_class = "PickupMessageInnerSchema"

    def __init__(
        self,
        id: str,
        message: str,
        **kwargs
    ):
        """
        Initialize  preview object.

        Args:
            id: Pickup message id
            message: Pickup message content

        """
        super().__init__(**kwargs)
        self.id = id
        self.message = message


class PickupMessageInnerSchema(BaseModelSchema):
    """Inner pickup message schema."""

    class Meta:
        """Inner pickup message schema metadata."""

        model_class = PickupMessageInner

    id = fields.Str(
        description="Pickup message id", required=True, example="123123123"
    )
    message = fields.Str(
        description="Pickup message content", required=False
    )
