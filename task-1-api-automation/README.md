# Task 1 — Zippopotam.us API Test Automation

Automated test suite for the single endpoint:

```
GET api.zippopotam.us/<country>/<postal-code>
```

Built with **Python + pytest + requests**.

## Test design

| File | Covers |
|---|---|
| `tests/test_valid_lookups.py` | Happy path: exact-value assertions on a known postal code, plus a parametrized sweep across countries with different postal code formats (numeric, alphanumeric, leading zeros, partial codes). |
| `tests/test_negative_cases.py` | Invalid postal code, invalid/nonexistent country, malformed input, and a basic check that error responses don't leak internals. |
| `tests/test_schema_validation.py` | JSON Schema contract check (required fields, types) — catches a field rename or shape change even for inputs we haven't hand-picked expected values for. |
| `tests/test_edge_cases.py` | Case sensitivity, trailing slashes, unsupported HTTP verbs, response-time sanity check, leading-zero postal codes. |

31 test cases total (several are parametrized, so this expands to more individual assertions at run time).

### Why this structure
- `src/zippopotam_client.py` isolates URL-building/session handling from the tests, so test files read as pure "given → when → then" and stay easy to extend.
- Fixtures (`conftest.py`) keep the client and reusable test data (`known_location`) out of individual test bodies.
- `pytest.ini` wires up an HTML report (`report.html`) by default and defines a `smoke` marker for a fast pre-merge subset (`pytest -m smoke`).

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
pytest                      # full suite, generates report.html
pytest -m smoke             # just the smoke subset
pytest tests/test_negative_cases.py -v
```

## A note on how this was verified

This suite was written and **collection-tested** (`pytest --collect-only`, 31/31 tests collect with no errors) in a sandboxed environment whose network egress is restricted to a small allowlist that doesn't include `api.zippopotam.us` — a live run there returns `403` at the proxy level, before the request ever reaches Zippopotam's servers. The suite has **not** been run end-to-end against the live API yet. Please run it in a normal environment with open internet access before relying on the results — I'd expect the happy-path and schema tests to pass as written, and the exploratory ones (case sensitivity, trailing slash, HTTP verb handling) to teach you something about the API's real behaviour either way.
