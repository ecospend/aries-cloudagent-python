from unittest import mock, TestCase

from asynctest import TestCase as AsyncTestCase

from ..pickup_message_inner import PickupMessageInner
from ....message_types import PROTOCOL_PACKAGE


test_id_data = "123123123"
test_message_data = {"content":"Hello"}

class TestPickupMessageInner(TestCase):
    def setUp(self):
        self.test_id = test_id_data
        self.test_message_content = test_message_data
        self.test_message = PickupMessageInner(id=self.test_id, message=self.test_message_content)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.id == self.test_id
        assert self.test_message.message == self.test_message_content

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.inner.pickup_message_inner.PickupMessageInnerSchema.load")
    def test_deserialize(self, mock_pickup_message_inner_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = PickupMessageInner.deserialize(obj)
        mock_pickup_message_inner_schema_load.assert_called_once_with(obj)

        assert msg is mock_pickup_message_inner_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.inner.pickup_message_inner.PickupMessageInnerSchema.dump")
    def test_serialize(self, mock_pickup_message_inner_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_pickup_message_inner_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_pickup_message_inner_schema_load.return_value


class TestPickupMessageSchema(AsyncTestCase):
    """Test pickup message inner schema."""

    async def test_make_model(self):
        pickup_message_inner = PickupMessageInner(id=test_id_data, message=test_message_data)
        data = pickup_message_inner.serialize()
        model_instance = PickupMessageInner.deserialize(data)
        assert type(model_instance) is type(pickup_message_inner)
