# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_hash(channel, hash_key, **kwargs):
    if not hash_key:
        raise KeyError("Brak odpowiedniego klucza hash_key dla channel_idx")

    # Sprawdź, czy istnieje odpowiedni klucz w hash_key
    if channel in hash_key:
        # Pobierz odpowiedni hash_key dla danego channel_idx
        kwargs["KEY"] = hash_key[channel]
    else:
        # Jeśli nie ma odpowiedniego klucza, zwróć None lub podobny komunikat błędu
        raise KeyError("Brak odpowiedniego klucza hash_key dla channel_idx")
    # Konkatenacja danych w formie string
    data_to_hash = "|".join(str(value) for value in kwargs.values())

    # Utworzenie obiektu SHA-256
    sha256 = hashlib.sha256(data_to_hash.encode("utf-8")).hexdigest()
    return sha256
