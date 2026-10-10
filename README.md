# entirius-py-autopay-sdk

A Python client for the Autopay payment gateway, part of Entirius, the open-source modular ecommerce platform.
It creates payment orders and lists the available payment gateways through one `Autopay` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-autopay-sdk.svg)](https://pypi.org/project/entirius-py-autopay-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-autopay-sdk.svg)](https://pypi.org/project/entirius-py-autopay-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-autopay-sdk/blob/develop/LICENSE)

## What it does

- Creates a payment order from an `Order` DTO (`create_order()`).
- Lists the payment gateways available for a `GatewayContext` (`get_gateway_list()`).
- Switches between the production and the test API (`use_sandbox()`, `get_api_url()`).
- Computes the SHA-256 request hash from a per-channel key (`autopay_sdk.utils.hash.generate_hash()`).

## Installation

```shell
uv add entirius-py-autopay-sdk
pip install entirius-py-autopay-sdk
```

The import name is `autopay_sdk`.

## Quick start

```python
from autopay_sdk.services.client import Autopay

autopay = Autopay(sandbox=True)
autopay.get_api_url()  # the test API; Autopay(sandbox=False) targets production
```

## Requirements

- Python 3.11 or newer.
- `requests` and `entirius-py-process-logger` (installed as dependencies).
- An Autopay merchant account; a test account for the sandbox.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-autopay-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is one of the payment gateway clients used by the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Checkout module: https://github.com/entirius/entirius-django-checkout
- Sibling gateway SDKs: https://github.com/entirius/entirius-py-payu-sdk, https://github.com/entirius/entirius-py-paynow-sdk, https://github.com/entirius/entirius-py-paypal-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-autopay-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-autopay-sdk/blob/develop/LICENSE.
