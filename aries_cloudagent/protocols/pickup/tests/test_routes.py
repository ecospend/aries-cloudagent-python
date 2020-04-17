from asynctest import TestCase as AsyncTestCase
from asynctest import mock as async_mock

from aiohttp import web as aio_web

from ....storage.error import StorageNotFoundError
from ....holder.base import BaseHolder
from ....messaging.request_context import RequestContext
from .. import routes as test_module


class TestPickupRoutes(AsyncTestCase):
    async def test_batch_pickup_messages(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"connection_id": "dummy"}
        mock.query = {"batch_size": 2}
        mock.app = {"request_context": "context"}

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_batch_size = async_mock.MagicMock()
            mock_pickup_manager.return_value.create_pickup_request.return_value = (
                mock_batch_size
            )

            await test_module.batch_pickup_messages(mock)

            mock_response.assert_called_once_with(
                {"batch_size": mock_batch_size}
            )


    async def test_get_status(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"connection_id": "dummy"}
        mock.app = {"request_context": "context"}

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_pickup_manager.return_value.create_pickup_request.return_value = ()

            await test_module.get_status(mock)

            mock_response.assert_called_once_with(
                {"succeed": True}
            )


    async def test_list_pickup_messages(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"connection_id": "dummy"}
        mock.app = {"request_context": "context"}
        mock.json = async_mock.CoroutineMock(
            return_value={
                "message_id_list": ["59f568ed-e8a7-4d9c-a652-781838672443"]
            }
        )

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_message_is_list = async_mock.MagicMock()
            mock_pickup_manager.return_value.create_list_request.return_value = (
                mock_message_is_list
            )

            await test_module.list_pickup_messages(mock)

            mock_response.assert_called_once_with(
                {"message_id_list": mock_message_is_list}
            )


    async def test_store_pickup_message(self):
        mock = async_mock.MagicMock()
        mock.app = {"request_context": "context"}
        mock.json = async_mock.CoroutineMock(
            return_value={
                "verkey": "2wUJCoyzkJz1tTxehfT7Usq5FgJz3EQHBQC7b2mXxbRZ",
                "message": {"content": "Hello"}
            }
        )

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            pickupMessage = async_mock.MagicMock()
            mock_pickup_manager.return_value.store_pickup_message.return_value = (
                pickupMessage
            )

            await test_module.store_pickup_message(mock)

            mock_response.assert_called_once_with(
                {"message_id": pickupMessage.message_id}
            )


    async def test_get_pickup_message_by_id(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"message_id": "dummy"}
        mock.app = {"request_context": "context"}

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            record = async_mock.MagicMock()
            mock_pickup_manager.return_value.get_pickup_message.return_value = (
                record
            )

            await test_module.get_pickup_message_by_id(mock)

            mock_response.assert_called_once_with(record.serialize())


    async def test_get_pickup_message_by_id_not_found(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"message_id": "dummy"}
        mock.app = {"request_context": "context"}

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager:
            
            # Emulate storage not found (bad message id)
            mock_pickup_manager.return_value.get_pickup_message.side_effect = StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.get_pickup_message_by_id(mock)

        
    async def test_get_pickup_messages_by_verkey(self):
        mock = async_mock.MagicMock()
        mock.query = {"verkey": "dummy"}
        mock.app = {"request_context": "context"}

        with async_mock.patch.object(
            test_module, "PickupManager", autospec=True
        ) as mock_pickup_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            records = async_mock.MagicMock()
            mock_pickup_manager.return_value.get_pickup_message_list.return_value = (
                records
            )

            await test_module.get_pickup_messages_by_verkey(mock)

            mock_response.assert_called_once_with(
                {"messages": [record.serialize() for record in records]}
            )


    async def test_get_pickup_messages_by_idlist(self):
            mock = async_mock.MagicMock()
            mock.app = {"request_context": "context"}
            mock.json = async_mock.CoroutineMock(
                return_value={
                    "message_id_list": ["59f568ed-e8a7-4d9c-a652-781838672443"]
                }
            )

            with async_mock.patch.object(
                test_module, "PickupManager", autospec=True
            ) as mock_pickup_manager, async_mock.patch.object(
                test_module.web, "json_response"
            ) as mock_response:
                
                pickupMessageList = []
                
                record = async_mock.MagicMock()
                mock_pickup_manager.return_value.get_pickup_message.return_value = (
                    record
                )

                pickupMessageList.append(record.serialize())

                await test_module.get_pickup_messages_by_idlist(mock)

                mock_response.assert_called_once_with(
                    {"messages": pickupMessageList}
                )


    async def test_get_pickup_messages_by_idlist_not_found(self):
            mock = async_mock.MagicMock()
            mock.app = {"request_context": "context"}
            mock.json = async_mock.CoroutineMock(
                return_value={
                    "message_id_list": ["59f568ed-e8a7-4d9c-a652-781838672443"]
                }
            )

            with async_mock.patch.object(
                test_module, "PickupManager", autospec=True
            ) as mock_pickup_manager:
                
                # Emulate storage not found (bad message id)
                mock_pickup_manager.return_value.get_pickup_message.side_effect = StorageNotFoundError()

                with self.assertRaises(test_module.web.HTTPNotFound):
                    await test_module.get_pickup_messages_by_idlist(mock)

    
    