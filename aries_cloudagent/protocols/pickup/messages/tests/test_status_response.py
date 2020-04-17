from unittest import mock, TestCase

from asynctest import TestCase as AsyncTestCase

from ..status_response import StatusResponse
from ...message_types import STATUS_RESPONSE, PROTOCOL_PACKAGE


class TestStatusResponse(TestCase):
    def setUp(self):
        self.test_message_count = 2
        self.test_message = StatusResponse(message_count=self.test_message_count)

    def test_init(self):
        """Test initialization."""
        assert self.test_message.message_count == self.test_message_count

    def test_type(self):
        """Test type."""
        assert self.test_message._type == STATUS_RESPONSE

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.status_response.StatusResponseSchema.load")
    def test_deserialize(self, mock_status_response_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = StatusResponse.deserialize(obj)
        mock_status_response_schema_load.assert_called_once_with(obj)

        assert msg is mock_status_response_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.status_response.StatusResponseSchema.dump")
    def test_serialize(self, mock_status_response_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_status_response_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_status_response_schema_load.return_value


class TestStatusResponseSchema(AsyncTestCase):
    """Test status response schema."""

    async def test_make_model(self):
        status_response = StatusResponse(message_count=2)
        data = status_response.serialize()
        model_instance = StatusResponse.deserialize(data)
        assert type(model_instance) is type(status_response)
