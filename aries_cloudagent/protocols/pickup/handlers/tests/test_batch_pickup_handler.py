import pytest
from asynctest import (
    mock as async_mock,
    TestCase as AsyncTestCase,
)

from .....messaging.request_context import RequestContext
from .....messaging.responder import MockResponder
from .....transport.inbound.receipt import MessageReceipt

from ...messages.batch_pickup_request import BatchPickupRequest
from ...handlers import batch_pickup_handler as handler


class TestBatchPickupHandler(AsyncTestCase):
    async def test_called(self):
        request_context = RequestContext()
        request_context.message = async_mock.MagicMock()
        request_context.message_receipt = MessageReceipt()

        with async_mock.patch.object(
            handler, "PickupManager", autospec=True
        ) as mock_pickup_mgr:
            mock_pickup_mgr.return_value.receive_pickup_request = async_mock.CoroutineMock(
                return_value="response"
            )
            request_context.message = BatchPickupRequest()
            request_context.connection_ready = True
            handler_inst = handler.BatchPickupHandler()
            responder = MockResponder()
            await handler_inst.handle(request_context, responder)

        mock_pickup_mgr.assert_called_once_with(request_context)
        mock_pickup_mgr.return_value.receive_pickup_request.assert_called_once_with()
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
            mock_pickup_mgr.return_value.receive_pickup_request = (
                async_mock.CoroutineMock()
            )
            request_context.message = BatchPickupRequest()
            request_context.connection_ready = False
            handler_inst = handler.BatchPickupHandler()
            responder = MockResponder()
            with self.assertRaises(handler.HandlerException):
                await handler_inst.handle(request_context, responder)

        assert not responder.messages