from asynctest import TestCase as AsyncTestCase
from asynctest import mock as async_mock

from ....config.injection_context import InjectionContext
from ....messaging.request_context import RequestContext
from ....ledger.base import BaseLedger
from ....messaging.responder import BaseResponder, MockResponder
from ....storage.error import StorageNotFoundError
from .. import routes as test_module

from ..manager import PickupManager
from ..models.pickup_message import PickupMessage
from ..messages.batch_pickup_request import BatchPickupRequest
from ..messages.status_request import StatusRequest
from ..messages.list_pickup_request import ListPickupRequest


class TestPickupManager(AsyncTestCase):
    async def setUp(self):
        self.context = RequestContext(
            base_context=InjectionContext(enforce_typing=False)
        )
        Ledger = async_mock.MagicMock(BaseLedger, autospec=True)
        self.ledger = Ledger()
        self.context.injector.bind_instance(BaseLedger, self.ledger)
        self.manager = PickupManager(self.context)

    async def test_store_pickup_message(self):
        message="dummy"
        verkey="dummy"
        with async_mock.patch.object(
            PickupMessage, "save", autospec=True
        ) as save_msg:
            stored_msg = await self.manager.store_pickup_message(
                verkey=verkey,
                message=message
                )
            save_msg.assert_called_once()

            assert stored_msg
            assert stored_msg.message == message
            assert stored_msg.verkey == verkey

    async def test_get_pickup_message(self):
        message_id="dummy"
        pickup_message = PickupMessage(
            message_id=message_id
        )
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_id",
            async_mock.CoroutineMock(return_value=pickup_message)
        ) as get_msg:
            stored_msg = await self.manager.get_pickup_message(
                message_id=message_id
                )
            get_msg.assert_called_once()
            assert stored_msg.message_id == message_id

    async def test_get_pickup_message_list(self):
        verkey="dummy"
        pickup_message = PickupMessage(
            verkey=verkey
        )
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_verkey",
            async_mock.CoroutineMock(return_value=pickup_message)
        ) as get_msg:
            stored_msg = await self.manager.get_pickup_message_list(
                verkey=verkey
                )
            get_msg.assert_called_once()
            assert stored_msg.verkey == verkey

    async def test_create_pickup_request(self):
        responder = MockResponder()
        self.context.injector.bind_instance(BaseResponder, responder)

        await self.manager.create_pickup_request(batch_size=2, connection_id="dummy")
        messages = responder.messages
        assert len(messages) == 1

    async def test_receive_pickup_request(self):
        verkey="dummy"
        created_at="dummy"
        message="dummy"
        pickup_request = BatchPickupRequest(batch_size=1)
        self.context.message = pickup_request
        self.context.message_receipt = async_mock.MagicMock()
        self.context.message_receipt.sender_verkey = verkey
        pickup_message_list = []
        pickup_message = PickupMessage(
            verkey=verkey,
            created_at=created_at,
            message=message
        )
        pickup_message_list.append(pickup_message)
        pickup_message_list.append(pickup_message) # for testing batch size < pickup message length
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_verkey",
            async_mock.CoroutineMock(return_value=pickup_message_list)
        ) as get_msg:
            response = await self.manager.receive_pickup_request(
                )
            get_msg.assert_called_once()
            assert response.messages_attach[0].message == message

    async def test_create_status_request(self):
        responder = MockResponder()
        self.context.injector.bind_instance(BaseResponder, responder)

        await self.manager.create_status_request(connection_id="dummy")
        messages = responder.messages
        assert len(messages) == 1

    async def test_receive_status_request(self):
        verkey="dummy"
        status_request = StatusRequest()
        self.context.message = status_request
        self.context.message_receipt = async_mock.MagicMock()
        self.context.message_receipt.sender_verkey = verkey
        pickup_message_list = []
        pickup_message = PickupMessage(
            verkey=verkey
        )
        pickup_message_list.append(pickup_message)
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_verkey",
            async_mock.CoroutineMock(return_value=pickup_message_list)
        ) as get_msg:
            response = await self.manager.receive_status_request(
                )
            get_msg.assert_called_once()
            assert response.message_count == 1

    async def test_create_list_request(self):
        responder = MockResponder()
        self.context.injector.bind_instance(BaseResponder, responder)
        message_id_list = async_mock.MagicMock()

        await self.manager.create_list_request(message_id_list=message_id_list, connection_id="dummy")
        messages = responder.messages
        assert len(messages) == 1

    async def test_receive_list_request(self):
        verkey="dummy"
        message_id="dummy"
        message="dummy"

        list_pickup_request = ListPickupRequest()
        list_pickup_request.message_ids = []
        list_pickup_request.message_ids.append(message_id)
        self.context.message = list_pickup_request

        self.context.message_receipt = async_mock.MagicMock()
        self.context.message_receipt.sender_verkey = verkey
        pickup_message = PickupMessage(
            verkey=verkey,
            message_id=message_id,
            message=message
        )
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_id",
            async_mock.CoroutineMock(return_value=pickup_message)
        ) as get_msg:
            response = await self.manager.receive_list_request(
                )
            get_msg.assert_called_once()
            assert response.messages_attach[0].message == message

    async def test_receive_list_request_not_found(self):
        verkey="dummy"
        message_id="dummy"

        list_pickup_request = ListPickupRequest()
        list_pickup_request.message_ids = []
        list_pickup_request.message_ids.append(message_id)
        self.context.message = list_pickup_request

        self.context.message_receipt = async_mock.MagicMock()
        self.context.message_receipt.sender_verkey = verkey
        
        with async_mock.patch.object(
            PickupMessage,
            "retrieve_by_id",
            async_mock.CoroutineMock(side_effect=StorageNotFoundError)
        ) as get_msg:

            response = await self.manager.receive_list_request()
            get_msg.assert_called_once()
            assert not response.messages_attach
