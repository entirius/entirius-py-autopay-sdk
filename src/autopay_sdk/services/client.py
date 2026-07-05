# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from urllib.parse import urlencode

import requests
from process_logger import ProcessLogger, ProcessLoggerMixin

from autopay_sdk import settings
from autopay_sdk.dto.gateway import GatewayContext
from autopay_sdk.dto.order import Order
from autopay_sdk.validators.response import (
    validate_autopay_create_order_success,
    validate_autopay_gateway_response,
    validate_autopay_get_method_success,
    validate_autopay_response,
)

logger_process = logging.getLogger(__name__)


class Autopay(ProcessLoggerMixin):
    sandbox: bool
    authorization = None

    def __init__(self, sandbox: bool, authorization=None):
        self.sandbox = sandbox
        self.authorization = authorization

    logger = ProcessLogger("AUTOPAY_SDK")

    def use_sandbox(self, flag: bool = True) -> None:
        self.sandbox = flag

    def is_sandbox(self) -> bool:
        return self.sandbox

    def get_api_url(self) -> str:
        if not self.sandbox:
            return settings.API_URL_PROD
        else:
            return settings.API_URL_TEST

    def _build_url(self, endpoint: str) -> str:
        return self.get_api_url() + endpoint

    def create_order(self, order: Order) -> (str, str):
        """
        Creates order in Autopay. If Succes you will recive Autopay internal order ID and redirect URI to complete transaction.
        """

        endpoint = "/payment"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "BmHeader": "pay-bm-continue-transaction-url"}

        # Kodowanie danych w formie application/x-www-form-urlencoded
        encoded_payload = urlencode(order)
        response = requests.request(method="POST", url=self._build_url(endpoint), headers=headers, data=encoded_payload)

        validation, response_body = validate_autopay_response(response)
        if validation:
            success = validate_autopay_create_order_success(response_body)
            if success:
                return response_body
        else:
            logger_process.error("Autopay API response failed")
            self.logger.error("Autopay API response failed")
            raise ValueError(f"The Autopay API responded with an error. Message: {response_body['message']}")

        # If nothing happend
        raise SystemError("Unknown Error")

    def get_gateway_list(self, gateway_context: GatewayContext):
        endpoint = "/gatewayList/v2"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = gateway_context.asdict()
        response = requests.request(method="POST", url=self._build_url(endpoint), headers=headers, json=payload)
        validation, response_body = validate_autopay_gateway_response(response)
        if validation:
            success = validate_autopay_get_method_success(response_body)
            if success:
                return response_body
        else:
            logger_process.error("Autopay API response failed")
            self.logger.error("Autopay API response failed")
            raise ValueError(f"The Autopay API responded with an error. Message: {response_body['message']}")
