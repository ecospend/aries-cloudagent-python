from unittest import mock, TestCase
from asynctest import TestCase as AsyncTestCase

from ..list_pickup_request import ListPickupRequest
from ...message_types import LIST_PICKUP_REQUEST, PROTOCOL_PACKAGE

test_id_data = ["59f568ed-e8a7-4d9c-a652-781838672443","2ff7b881-2620-4c27-a5b0-4dca46d4c778"]

class TestListPickupRequest(TestCase):
    def setUp(self):
        self.test_message = ListPickupRequest(message_ids=test_id_data)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.message_ids == test_id_data

    def test_type(self):
        """Test type."""
        assert self.test_message._type == LIST_PICKUP_REQUEST

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.list_pickup_request.ListPickupRequestSchema.load")
    def test_deserialize(self, mock_list_pickup_request_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = ListPickupRequest.deserialize(obj)
        mock_list_pickup_request_schema_load.assert_called_once_with(obj)

        assert msg is mock_list_pickup_request_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.list_pickup_request.ListPickupRequestSchema.dump")
    def test_serialize(self, mock_list_pickup_request_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_list_pickup_request_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_list_pickup_request_schema_load.return_value


class ListPickupRequestSchema(AsyncTestCase):
    """Test list pickup request schema."""

    async def test_make_model(self):
        list_pickup_request = ListPickupRequest(message_ids=test_id_data)
        data = list_pickup_request.serialize()
        model_instance = ListPickupRequest.deserialize(data)
        assert type(model_instance) is type(list_pickup_request)
