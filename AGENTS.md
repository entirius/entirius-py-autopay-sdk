# AGENTS.md

Autopay payment gateway SDK — distribution `entirius-py-autopay-sdk`, import `autopay_sdk`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `autopay_sdk` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`src/autopay_sdk/`: `services/client.py` holds the `Autopay` client (order creation, gateway list) over the
Autopay REST API; DTOs live in `dto/`, the request hash in `utils/hash.py`, response checks in `validators/`.
`settings.py` holds the public API URLs (test and production). Runtime dependencies: `requests`,
`entirius-py-process-logger`. The test suite is a local import check; it makes no network call.
