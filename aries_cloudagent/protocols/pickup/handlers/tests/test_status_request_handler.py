import pytest
from asynctest import (
    mock as async_mock,
    TestCase as AsyncTestCase,
)

from .....messaging.request_context import RequestContext
from .....messaging.responder import MockResponder
from .....transport.inbound.receipt import MessageReceipt

from ...messages.status_request import StatusRequest
from ...handlers import status_request_handler as handler


class TestStatusRequestHandler(AsyncTestCase):
    async def test_called(self):
        request_context = RequestContext()
        request_context.message = async_mock.MagicMock()
        request_context.message_receipt = MessageReceipt()

        with async_mock.patch.object(
            handler, "PickupManager", autospec=True
        ) as mock_pickup_mgr:
            mock_pickup_mgr.return_value.receive_status_request = async_mock.CoroutineMock(
                return_value="response"
            )
            request_context.message = StatusRequest()
            request_context.connection_ready = True
            handler_inst = handler.StatusRequestHandler()
            responder = MockResponder()
            await handler_inst.handle(request_context, responder)

        mock_pickup_mgr.assert_called_once_with(request_context)
        mock_pickup_mgr.return_value.receive_status_request.assert_called_once_with()
        messages = responder.messages
        assert len(messages) == 1
        (result, target) = messages[0]
        assert result == "response"
        assert target == {}

    async def test_called_not_ready(self):
        request_context = RequestContext()
        request_context.message_receipt = MessageReceipt()

        with async_mock.patch.object(
            handler, "PickupManager", autospec=True
        ) as mock_pickup_mgr:
            mock_pickup_mgr.return_value.receive_status_request = (
                async_mock.CoroutineMock()
            )
            request_context.message = StatusRequest()
            request_context.connection_ready = False
            handler_inst = handler.StatusRequestHandler()
            responder = MockResponder()
            with self.assertRaises(handler.HandlerException):
                await handler_inst.handle(request_context, responder)

        assert not responder.messages