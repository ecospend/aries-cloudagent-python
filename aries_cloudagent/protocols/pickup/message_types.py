"""Message type identifiers for pickup protocol."""

PROTOCOL_URI = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0"

STATUS_REQUEST = f"{PROTOCOL_URI}/status_request"
STATUS_RESPONSE = f"{PROTOCOL_URI}/status_response"
BATCH_PICKUP_REQUEST = f"{PROTOCOL_URI}/batch_pickup_request"
BATCH_PICKUP_RESPONSE = f"{PROTOCOL_URI}/batch_pickup_response"
LIST_PICKUP_REQUEST = f"{PROTOCOL_URI}/list_pickup_request"
LIST_PICKUP_RESPONSE = f"{PROTOCOL_URI}/list_pickup_response"

NEW_PROTOCOL_URI = "https://didcomm.org/messagepickup/0.1"

NEW_STATUS_REQUEST = f"{NEW_PROTOCOL_URI}/status_request"
NEW_STATUS_RESPONSE = f"{PROTOCOL_URI}/status_response"
NEW_BATCH_PICKUP_REQUEST = f"{NEW_PROTOCOL_URI}/batch_pickup_request"
NEW_BATCH_PICKUP_RESPONSE = f"{NEW_PROTOCOL_URI}/batch_pickup_response"
NEW_LIST_PICKUP_REQUEST = f"{PROTOCOL_URI}/list_pickup_request"
NEW_LIST_PICKUP_RESPONSE = f"{PROTOCOL_URI}/list_pickup_response"

PROTOCOL_PACKAGE = "aries_cloudagent.protocols.pickup"

MESSAGE_TYPES = {
    STATUS_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.status_request.StatusRequest"
    ),
    STATUS_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.status_response.StatusResponse"
    ),
    BATCH_PICKUP_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.batch_pickup_request.BatchPickupRequest"
    ),
    BATCH_PICKUP_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.batch_pickup_response.BatchPickupResponse"
    ),
    LIST_PICKUP_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.list_pickup_request.ListPickupRequest"
    ),
    LIST_PICKUP_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.list_pickup_response.ListPickupResponse"
    ),
    NEW_STATUS_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.status_request.StatusRequest"
    ),
    NEW_STATUS_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.status_response.StatusResponse"
    ),
    NEW_BATCH_PICKUP_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.batch_pickup_request.BatchPickupRequest"
    ),
    NEW_BATCH_PICKUP_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.batch_pickup_response.BatchPickupResponse"
    ),
    NEW_LIST_PICKUP_REQUEST: (
        f"{PROTOCOL_PACKAGE}.messages.list_pickup_request.ListPickupRequest"
    ),
    NEW_LIST_PICKUP_RESPONSE: (
        f"{PROTOCOL_PACKAGE}.messages.list_pickup_response.ListPickupResponse"
    ),
}
