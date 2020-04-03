"""Pickup admin routes."""
from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema

from .manager import PickupManager

from ...storage.error import StorageNotFoundError


class StorePickupMessageSchema(Schema):
    """Request schema for storing a pickup message."""

    message = fields.Dict(
        description=("Message content"),
        required=False,
        keys=fields.Str(example="content"),
        values=fields.Str(example="Hello"),
    )
    verkey = fields.Str(
        description="Recipient verkey",
        example="2wUJCoyzkJz1tTxehfT7Usq5FgJz3EQHBQC7b2mXxbRZ"
        )


class PickupMessageSchema(Schema):
    """Result schema for a pickup message query."""

    message_id = fields.Str(
        description="Pickup message identifier"
    )
    message = fields.Dict(
        description="Pickup message content"
    )


class PickupMessageIdSchema(Schema):
    """Request schema for getting pickup message list."""

    message_id = fields.Str(
        description="Pickup message identifier"
    )


class PickupMessageIdListSchema(Schema):
    """Request schema for getting pickup message list."""

    message_id_list = fields.List(
        fields.Str(description="Pickup message identifier")
        )


class PickupMessageListSchema(Schema):
    """Result schema for a pickup message query."""

    results = fields.List(fields.Nested(PickupMessageSchema()))


class PickupMessageListResponseSchema(Schema):
    """Result schema for pickup list query."""

    message_id_list = fields.Str(
        description="List of successfully requested message ids"
    )


class BatchResponseSchema(Schema):
    """Result schema for batch pickup message query."""

    batch_size = fields.Int(
        description="Requested pickup message count"
    )


class StatusResponseSchema(Schema):
    """Result schema for a status of messages query."""

    succeed = fields.Bool(
        description="Pickup messages status query operation is comleted"
    )


@docs(tags=["pickup"], summary="Store a pickup message")
@request_schema(StorePickupMessageSchema())
async def store_pickup_message(request: web.BaseRequest):
    """
    Request handler for storing a pickup message.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message id

    """

    pickup_message_json = await request.json()

    verkey = pickup_message_json.get('verkey')
    message = pickup_message_json.get('message')

    context = request.app["request_context"]

    pickupManager = PickupManager(context)

    pickupMessage = await pickupManager.store_pickup_message(
        message=message, verkey=verkey
    )

    response = {'message_id': pickupMessage.message_id}

    return web.json_response(response)


@docs(tags=["pickup"], summary="Fetch a single pickup message")
@response_schema(PickupMessageSchema(), 200)
async def get_pickup_message_by_id(request: web.BaseRequest):
    """
    Request handler for fetching a single pickup message.

    Args:
        request: aiohttp request object

    Returns:
        The pickup message response

    """
    context = request.app["request_context"]
    message_id = request.match_info["message_id"]

    pickupManager = PickupManager(context)

    try:
        record = await pickupManager.get_pickup_message(message_id=message_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()
    return web.json_response(record.serialize())


@docs(
    tags=["pickup"],
    summary="Get pickup message list by verkey",
    parameters=[
        {
            "name": "verkey",
            "in": "query",
            "schema": {"type": "string"},
            "required": True,
        },
    ],
    )
@response_schema(PickupMessageListSchema(), 200)
async def get_pickup_messages_by_verkey(request: web.BaseRequest):
    """
    Request handler for getting a pickup message list.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message list

    """

    context = request.app["request_context"]
    verkey = request.query.get("verkey")

    pickupManager = PickupManager(context)
    records = await pickupManager.get_pickup_message_list(verkey)
    return web.json_response({"messages": [record.serialize() for record in records]})


@docs(tags=["pickup"], summary="Get pickup message list by id list")
@request_schema(PickupMessageIdListSchema())
@response_schema(PickupMessageListSchema(), 200)
async def get_pickup_messages_by_idlist(request: web.BaseRequest):
    """
    Request handler for getting a pickup message list.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message list

    """
    context = request.app["request_context"]
    pickupManager = PickupManager(context)

    pickupMessageList = []
    id_list_json = await request.json()

    for message_id in id_list_json.get('message_id_list'):
        try:
            record = await pickupManager.get_pickup_message(
                message_id=message_id
                )
        except StorageNotFoundError:
            raise web.HTTPNotFound()
        if record:
            pickupMessageList.append(record.serialize())

    return web.json_response({"messages": pickupMessageList})


@docs(
    tags=["pickup"],
    summary="Get batch size of pickup messages",
    parameters=[
        {
            "name": "batch_size",
            "in": "query",
            "schema": {"type": "int"},
            "required": True,
        },
    ],
    )
@response_schema(BatchResponseSchema(), 200)
async def batch_pickup_messages(request: web.BaseRequest):
    """
    Request handler for getting batch of pickup messages.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message list

    """

    context = request.app["request_context"]
    batch_size = request.query.get("batch_size")
    connection_id = request.match_info["connection_id"]

    pickupManager = PickupManager(context)

    batch_size = await pickupManager.create_pickup_request(
        batch_size=batch_size,
        connection_id=connection_id
    )

    return web.json_response({"batch_size": batch_size})


@docs(tags=["pickup"], summary="Get pickup messages status of recipient")
@response_schema(StatusResponseSchema(), 200)
async def get_status(request: web.BaseRequest):
    """
    Request handler for pickup messages status.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message status

    """

    context = request.app["request_context"]
    connection_id = request.match_info["connection_id"]

    pickupManager = PickupManager(context)

    await pickupManager.create_status_request(
        connection_id=connection_id
    )

    return web.json_response({"succeed": True})


@docs(
    tags=["pickup"],
    summary="Get pickup message list of given message id list"
    )
@request_schema(PickupMessageIdListSchema())
@response_schema(PickupMessageListResponseSchema(), 200)
async def list_pickup_messages(request: web.BaseRequest):
    """
    Request handler for getting pickup message list.

    Args:
        request: aiohttp request object

    Returns:
        Stored pickup message list

    """

    context = request.app["request_context"]
    connection_id = request.match_info["connection_id"]
    id_list_json = await request.json()

    pickupManager = PickupManager(context)

    message_id_list = []

    for message_id in id_list_json.get('message_id_list'):
        message_id_list.append(message_id)

    messages = await pickupManager.create_list_request(
        message_id_list=message_id_list,
        connection_id=connection_id
    )

    return web.json_response({"message_id_list": messages})


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.post("/pickup/store-message", store_pickup_message),
            web.post("/pickup/messages/by-verkey", get_pickup_messages_by_verkey),
            web.post("/pickup/messages/by-idlist", get_pickup_messages_by_idlist),
            web.post("/pickup/messages/{message_id}", get_pickup_message_by_id),
            web.post("/pickup/{connection_id}/batch_pickup", batch_pickup_messages),
            web.post("/pickup/{connection_id}/status", get_status),
            web.post("/pickup/{connection_id}/list_pickup", list_pickup_messages),
        ]
    )
