"""
Edge cases and exploratory checks that don't fit neatly into "positive"
or "negative" - things worth knowing about the API's actual behaviour
so the team isn't surprised by it in production.
"""
import time

import pytest


def test_country_code_is_case_insensitive(api_client):
    """Worth knowing either way: if the API silently accepts 'US' and
    'us' as the same thing, callers shouldn't need to normalise case
    themselves. If it isn't case-insensitive, that's a UX gap worth
    flagging to the team, not a bug in this test."""
    lower = api_client.get_location("us", "90210")
    upper = api_client.get_location("US", "90210")

    assert lower.status_code == 200
    assert upper.status_code == 200
    assert lower.json() == upper.json()


def test_trailing_slash_is_handled_consistently(api_client):
    with_slash = api_client.get_location("us", "90210/")
    without_slash = api_client.get_location("us", "90210")

    assert without_slash.status_code == 200
    # A trailing slash should either resolve the same way or fail
    # cleanly - never a 500.
    assert with_slash.status_code in (200, 301, 302, 404)


def test_response_time_is_reasonable(api_client, known_location):
    """A lightweight performance guardrail, not a load test: catches a
    pathological regression (e.g. an accidental N+1 lookup) without
    needing dedicated performance tooling."""
    start = time.monotonic()
    response = api_client.get_location(known_location["country"], known_location["postal_code"])
    elapsed = time.monotonic() - start

    assert response.status_code == 200
    assert elapsed < 3.0, f"request took {elapsed:.2f}s, expected under 3s"


@pytest.mark.parametrize("method_name", ["post", "put", "delete", "patch"])
def test_unsupported_http_methods_are_rejected(api_client, known_location, method_name):
    """The endpoint is documented as a read-only lookup; verify other
    verbs don't silently succeed (which could indicate an
    unintentionally writable/proxied route)."""
    url = f"{api_client.base_url}/{known_location['country']}/{known_location['postal_code']}"
    method = getattr(api_client.session, method_name)
    response = method(url, timeout=api_client.timeout)

    assert response.status_code in (404, 405)


def test_leading_zeros_in_postal_code_are_preserved(api_client):
    """Postal codes aren't numbers (leading zeros matter, e.g. German
    '01067'). Confirms the API treats the path segment as a string,
    not an integer that would silently drop the zero."""
    response = api_client.get_location("de", "01067")

    assert response.status_code == 200
    assert response.json()["post code"] == "01067"
