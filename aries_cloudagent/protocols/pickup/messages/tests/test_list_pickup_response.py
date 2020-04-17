from unittest import mock, TestCase
from asynctest import TestCase as AsyncTestCase

from ..inner.pickup_message_inner import PickupMessageInner
from ..list_pickup_response import ListPickupResponse
from ...message_types import LIST_PICKUP_RESPONSE, PROTOCOL_PACKAGE

test_id_data = "59f568ed-e8a7-4d9c-a652-781838672443"
test_message_data = {"content":"Hello"}
test_inner_message = PickupMessageInner(id=test_id_data, message=test_message_data)

class TestListPickupResponse(TestCase):
    def setUp(self):
        self.test_message = ListPickupResponse()
        self.test_message.messages_attach.append(test_inner_message)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.messages_attach[0] == test_inner_message

    def test_type(self):
        """Test type."""
        assert self.test_message._type == LIST_PICKUP_RESPONSE

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.list_pickup_response.ListPickupResponseSchema.load")
    def test_deserialize(self, mock_list_pickup_response_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = ListPickupResponse.deserialize(obj)
        mock_list_pickup_response_schema_load.assert_called_once_with(obj)

        assert msg is mock_list_pickup_response_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.list_pickup_response.ListPickupResponseSchema.dump")
    def test_serialize(self, mock_list_pickup_response_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_list_pickup_response_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_list_pickup_response_schema_load.return_value


class TestListPickupResponseSchema(AsyncTestCase):
    """Test list pickup response schema."""

    async def test_make_model(self):
        list_pickup_response = ListPickupResponse()
        list_pickup_response.messages_attach.append(test_inner_message)
        data = list_pickup_response.serialize()
        model_instance = ListPickupResponse.deserialize(data)
        assert type(model_instance) is type(list_pickup_response)
