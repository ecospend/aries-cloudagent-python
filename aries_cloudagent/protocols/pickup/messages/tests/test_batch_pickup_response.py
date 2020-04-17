from unittest import mock, TestCase
from asynctest import TestCase as AsyncTestCase

from ..inner.pickup_message_inner import PickupMessageInner
from ..batch_pickup_response import BatchPickupResponse
from ...message_types import BATCH_PICKUP_RESPONSE, PROTOCOL_PACKAGE

test_id_data = "59f568ed-e8a7-4d9c-a652-781838672443"
test_message_data = {"content":"Hello"}
test_inner_message = PickupMessageInner(id=test_id_data, message=test_message_data)

class TestBatchPickupResponse(TestCase):
    def setUp(self):
        self.test_message = BatchPickupResponse()
        self.test_message.messages_attach.append(test_inner_message)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.messages_attach[0] == test_inner_message

    def test_type(self):
        """Test type."""
        assert self.test_message._type == BATCH_PICKUP_RESPONSE

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.batch_pickup_response.BatchPickupResponseSchema.load")
    def test_deserialize(self, mock_batch_pickup_response_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = BatchPickupResponse.deserialize(obj)
        mock_batch_pickup_response_schema_load.assert_called_once_with(obj)

        assert msg is mock_batch_pickup_response_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.batch_pickup_response.BatchPickupResponseSchema.dump")
    def test_serialize(self, mock_batch_pickup_response_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_batch_pickup_response_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_batch_pickup_response_schema_load.return_value


class TestBatchPickupResponseSchema(AsyncTestCase):
    """Test batch pickup response schema."""

    async def test_make_model(self):
        batch_pickup_response = BatchPickupResponse()
        batch_pickup_response.messages_attach.append(test_inner_message)
        data = batch_pickup_response.serialize()
        model_instance = BatchPickupResponse.deserialize(data)
        assert type(model_instance) is type(batch_pickup_response)
