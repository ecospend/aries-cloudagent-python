import asyncio
import json
import string
import random

from pyfcm.errors import AuthenticationError
from aiohttp.test_utils import unittest_run_loop
from asynctest import TestCase as AsyncTestCase, mock as async_mock
from aiohttp import web, WSMsgType

from ....config.injection_context import InjectionContext

from ..push import PushTransport
from ..base import OutboundTransportError


class TestPushTransport(AsyncTestCase):
    async def test_setup(self):
        self.context = InjectionContext()
        self.context.settings['transport.push_api_key'] = "API_KEY_FOR_PUSH"

    @unittest_run_loop
    async def test_handle_message(self):

        self.context = InjectionContext()
        self.context.settings['transport.push_api_key'] = "API_KEY_FOR_PUSH"

        async def send_message(transport, payload, endpoint: str):
            async with transport:
                await transport.handle_message(self.context, payload, endpoint)

        transport = PushTransport()
        try:
            await asyncio.wait_for(send_message(
                transport,
                "{}",
                endpoint="push://TEST_ID"
            ), 5.0)
            assert self.message_results == [{}]
        except OutboundTransportError as e:
            assert str(e) == "Push message couldn't be delivered"
        except AuthenticationError as e:
            pass
        assert transport.push_key == self.context.settings['transport.push_api_key']

        letters = string.ascii_lowercase
        long_message = ''.join(random.choice(letters) for i in range(4000))
        try:
            await asyncio.wait_for(send_message(
                transport,
                long_message,
                endpoint="push://TEST_ID"
            ), 5.0)
            assert self.message_results == [{}]
        except OutboundTransportError as e:
            assert str(e) == "Data size exceed push notification limits"