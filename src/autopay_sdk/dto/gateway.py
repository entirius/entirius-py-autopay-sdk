# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from autopay_sdk.dto import DTO


@dataclass
class GatewayContext(DTO):
    ServiceID: int
    MessageID: str
    Hash: str
    Currencies: str
