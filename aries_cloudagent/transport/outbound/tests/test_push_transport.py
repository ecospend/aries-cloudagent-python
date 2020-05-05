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
from ..base import OutboundTransportError, PushDataSizeExceedError


class TestPushTransport(AsyncTestCase):
    async def test_setup(self):
        self.context = InjectionContext()

    @unittest_run_loop
    async def test_handle_message(self):

        self.context = InjectionContext()

        async def send_message(transport, payload, endpoint: str):
            async with transport:
                await transport.handle_message(self.context, payload, endpoint)

        transport = PushTransport()
        try:
            transport.dry_run = True
            await asyncio.wait_for(send_message(
                transport,
                b'Test Message',
                endpoint="push://TEST_ID"
            ), 5.0)
            assert self.message_results == [{}]
        except OutboundTransportError as e:
            assert not str(e) == "API ERROR"
        except AuthenticationError as e:
            pass

        letters = string.ascii_lowercase
        long_message = ''.join(random.choice(letters) for i in range(4000))
        try:
            await asyncio.wait_for(send_message(
                transport,
                long_message.encode('utf-8'),
                endpoint="push://TEST_ID"
            ), 5.0)
            assert self.message_results == [{}]
        except PushDataSizeExceedError as e:
            assert str(e) == "Data size exceed push notification limits"