import pytest
from asynctest import (
    mock as async_mock,
    TestCase as AsyncTestCase,
)

from .....messaging.request_context import RequestContext
from .....messaging.responder import MockResponder
from .....transport.inbound.receipt import MessageReceipt

from ...messages.list_pickup_response import ListPickupResponse
from ...handlers import list_pickup_response_handler as handler


class ListPickupResponseHandler(AsyncTestCase):
    async def test_called(self):
        request_context = RequestContext()
        request_context.message = async_mock.MagicMock()
        request_context.message_receipt = MessageReceipt()

        request_context.message = ListPickupResponse()
        request_context.connection_ready = True
        handler_inst = handler.ListPickupResponseHandler()
        responder = MockResponder()
        await handler_inst.handle(request_context, responder)

    async def test_called_not_ready(self):
        request_context = RequestContext()
        request_context.message_receipt = MessageReceipt()

        request_context.message = ListPickupResponse()
        request_context.connection_ready = False
        handler_inst = handler.ListPickupResponseHandler()
        responder = MockResponder()
        with self.assertRaises(handler.HandlerException):
            await handler_inst.handle(request_context, responder)

        assert not responder.messages