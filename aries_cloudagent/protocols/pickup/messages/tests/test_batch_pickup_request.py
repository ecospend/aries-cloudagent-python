from unittest import mock, TestCase

from asynctest import TestCase as AsyncTestCase

from ..batch_pickup_request import BatchPickupRequest
from ...message_types import BATCH_PICKUP_REQUEST, PROTOCOL_PACKAGE


class TestBatchPickupRequest(TestCase):
    def setUp(self):
        self.test_batch_size = 2
        self.test_message = BatchPickupRequest(batch_size=self.test_batch_size)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.batch_size == self.test_batch_size

    def test_type(self):
        """Test type."""
        assert self.test_message._type == BATCH_PICKUP_REQUEST

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.batch_pickup_request.BatchPickupRequestSchema.load")
    def test_deserialize(self, mock_batch_pickup_request_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = BatchPickupRequest.deserialize(obj)
        mock_batch_pickup_request_schema_load.assert_called_once_with(obj)

        assert msg is mock_batch_pickup_request_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.batch_pickup_request.BatchPickupRequestSchema.dump")
    def test_serialize(self, mock_batch_pickup_request_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_batch_pickup_request_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_batch_pickup_request_schema_load.return_value


class TestBatchPickupRequestSchema(AsyncTestCase):
    """Test batch pickup request schema."""

    async def test_make_model(self):
        batch_pickup_request = BatchPickupRequest(batch_size=2)
        data = batch_pickup_request.serialize()
        model_instance = BatchPickupRequest.deserialize(data)
        assert type(model_instance) is type(batch_pickup_request)
