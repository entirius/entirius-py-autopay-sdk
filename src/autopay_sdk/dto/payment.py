# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import asdict, dataclass, is_dataclass


@dataclass
class DTO:
    def to_dict(self):
        return asdict(self, dict_factory=lambda x: x.to_dict() if is_dataclass(x) else x)
