# autopay-sdk

Autopay (BLIK / card) payment gateway SDK — transactions and card operations over the Autopay REST API.

## Installation

```shell
pip install entirius-py-autopay-sdk
```

## Usage

```python
from autopay_sdk.services.client import Autopay

autopay = Autopay(...)
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
