# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
import xml.etree.ElementTree as ET

from requests import Response

logger_process = logging.getLogger(__name__)


def validate_autopay_response(response: Response) -> (bool, dict):
    response_tree = ET.fromstring(response.content)

    if response.status_code == 200:
        status_element = response_tree.find(".//status")
        confirmation_element = response_tree.find(".//confirmation")
        if status_element is not None and status_element.text == "PENDING":
            order_id = response_tree.find(".//orderID").text
            redirect_url = response_tree.find(".//redirecturl").text
            remote_id = response_tree.find(".//remoteID").text
            return True, {
                "status": "PENDING",
                "order_id": order_id,
                "redirect_url": redirect_url,
                "remote_id": remote_id,
            }
        elif confirmation_element is not None and confirmation_element.text == "NOTCONFIRMED":
            validaion, error_message = validate_autopay_response_body_when_error(confirmation_element, response_tree)
            return validaion, error_message
        else:
            # Obsługa normalnej odpowiedzi
            return True, response_tree

    if response.status_code in [400, 401, 403, 404, 500]:
        validation, error_message = validate_autopay_response_body_when_error(response_tree)
        if validation:
            if response.status_code == 400:
                raise ValueError(error_message)
            elif response.status_code == 401:
                raise ConnectionError(error_message)
            elif response.status_code == 403:
                raise PermissionError(error_message)
            elif response.status_code == 404:
                raise ValueError(error_message)
            elif response.status_code == 500:
                raise SystemError(error_message)

    return False, response_tree


def validate_autopay_gateway_response(response: Response) -> (bool, dict):
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        response_tree = ET.fromstring(response.content)

    if response.status_code == 200:
        service_id = response_json.get("serviceID")
        message_id = response_json.get("messageID")
        gateway_list = response_json.get("gatewayList")
        hash = response_json.get("hash")
        return True, {
            "status": "OK",
            "serviceID": service_id,
            "message_id": message_id,
            "gateway_list": gateway_list,
            "hash": hash,
        }

    if response.status_code in [400, 401, 403, 404, 500]:
        validation, error_message = validate_autopay_response_body_when_error(response_tree)
        if validation:
            if response.status_code == 400:
                raise ValueError(error_message)
            elif response.status_code == 401:
                raise ConnectionError(error_message)
            elif response.status_code == 403:
                raise PermissionError(error_message)
            elif response.status_code == 404:
                raise ValueError(error_message)
            elif response.status_code == 500:
                raise SystemError(error_message)

    return False, response_tree


def validate_autopay_response_body_when_error(confirmation_element, response_tree) -> (bool, str):
    order_id = response_tree.find(".//orderID")
    reason_element = response_tree.find(".//reason")
    hash_element = response_tree.find(".//hash")
    order_id = order_id.text if order_id is not None else ""
    reason = reason_element.text if reason_element is not None else ""
    hash_value = hash_element.text if hash_element is not None else ""
    msg = f"Autopay transaction not confirmed: order_id: {order_id} - {reason} (hash: {hash_value})"
    return False, {
        "status": confirmation_element,
        "order_id": order_id,
        "reason": reason,
        "hash": hash_value,
        "message": msg,
    }


def validate_autopay_create_order_success(response_body: dict):
    if response_body.get("status") == "PENDING":
        return True
    return False


def validate_autopay_get_method_success(response_body) -> bool:
    if "status" in response_body and response_body["status"] == "OK":
        if "gateway_list" in response_body and len(response_body["gateway_list"]) > 0:
            return True  # Wszystkie bramki są poprawne
        else:
            return False
    else:
        return False  # Nie spełnione warunki dla sukcesu
