from unittest import TestCase as UnitTestCase
from .....config.injection_context import InjectionContext
from .....messaging.request_context import RequestContext
from .....storage.basic import BasicStorage, StorageRecord
from .....storage.base import BaseStorage
from asynctest import TestCase as AsyncTestCase, mock as async_mock
from .....cache.base import BaseCache
import json

from ..pickup_message import PickupMessage


class TestPickupMessageUnit(UnitTestCase):
    def test_pickup_message(self):
        pickup_message = PickupMessage(
            message_id="msgid",
            target_url="targeturl",
            verkey="verkey",
            message={"content": "Hello"}
        )
       
        assert pickup_message.message_id == "msgid"
        assert pickup_message.message_query == "msgid"
        assert pickup_message.record_value == {
            "target_url":"targeturl",
            "verkey":"verkey",
            "message":{"content": "Hello"}
        }

class TestPickupMessageasync(AsyncTestCase):
    async def test_retrieve_by_verkey(self):
        context = InjectionContext(enforce_typing=False)
        mock_storage = async_mock.MagicMock(BaseStorage, autospec=True)
        context.injector.bind_instance(BaseStorage, mock_storage)
        record_verkey = "verkey"
        record_value = {"message": {"content": "Hello"}}
        tag_filter = {"verkey": "verkey"}
        stored = StorageRecord(
            PickupMessage.RECORD_TYPE, json.dumps(record_value), {}, record_verkey
        )

        mock_storage.search_records.return_value.__aiter__.return_value = [stored]
        result = await PickupMessage.retrieve_by_verkey(context, record_verkey)
        mock_storage.search_records.assert_called_once_with(
            PickupMessage.RECORD_TYPE, tag_filter, None, {"retrieveTags": False}
        )
        
        assert result and isinstance(result[0], PickupMessage)
        assert result[0].message == record_value.get("message")
   