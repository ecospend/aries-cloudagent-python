from unittest import mock, TestCase

from asynctest import TestCase as AsyncTestCase

from ..status_request import StatusRequest
from ...message_types import STATUS_REQUEST, PROTOCOL_PACKAGE


class TestStatusRequest(TestCase):
    def setUp(self):
        self.test_message = StatusRequest()

    def test_type(self):
        """Test type."""
        assert self.test_message._type == STATUS_REQUEST

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.status_request.StatusRequestSchema.load")
    def test_deserialize(self, mock_status_request_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = StatusRequest.deserialize(obj)
        mock_status_request_schema_load.assert_called_once_with(obj)

        assert msg is mock_status_request_schema_load.return_value

    @mock.patch(f"{PROTOCOL_PACKAGE}.messages.status_request.StatusRequestSchema.dump")
    def test_serialize(self, mock_status_request_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_message.serialize()
        mock_status_request_schema_load.assert_called_once_with(self.test_message)

        assert msg_dict is mock_status_request_schema_load.return_value


class TestStatusRequestSchema(AsyncTestCase):
    """Test status request schema."""

    async def test_make_model(self):
        status_request = StatusRequest()
        data = status_request.serialize()
        model_instance = StatusRequest.deserialize(data)
        assert type(model_instance) is type(status_request)
