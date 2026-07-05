# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, fields

from autopay_sdk.dto import DTO


@dataclass
class Order(DTO):
    ServiceID: str
    OrderID: str
    Amount: str
    Hash: str

    Description: str | None = None
    GatewayID: int | None = 0
    Currency: str | None = "PLN"
    CustomerEmail: str | None = None
    ValidityTime: str | None = None
    LinkValidityTime: str | None = None
    CustomerIP: str | None = None
    Title: str | None = None

    def exclude_none(self, field):
        return getattr(self, field.name) is not None

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in fields(self) if self.exclude_none(field)}
