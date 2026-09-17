"""
Negative-path test cases: the endpoint should fail predictably and
informatively for bad input, rather than 500ing or silently returning
wrong data.
"""
import pytest


def test_invalid_postal_code_returns_404(api_client):
    response = api_client.get_location("us", "00000000")
    assert response.status_code == 404


def test_invalid_country_code_returns_404(api_client):
    response = api_client.get_location("zz", "90210")
    assert response.status_code == 404


def test_nonexistent_country_name_returns_404(api_client):
    response = api_client.get_location("narnia", "90210")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "country, postal_code",
    [
        ("us", ""),           # missing postal code
        ("", "90210"),        # missing country
        ("us", "!!!!!"),      # invalid characters
        ("123", "90210"),     # numeric "country"
        ("us", "9"),          # too short to be a real US zip
    ],
)
def test_malformed_input_does_not_return_200(api_client, country, postal_code):
    """None of these should be treated as a valid lookup. We assert
    "not 200" rather than a single status code because malformed URLs
    (e.g. an empty path segment) can 404 via routing rather than via
    the endpoint's own "not found" logic - both are acceptable, a 200
    is not."""
    response = api_client.get_location(country, postal_code)
    assert response.status_code != 200


def test_error_response_does_not_leak_server_internals(api_client):
    """A basic sanity/security check: a 404 shouldn't dump a stack
    trace or internal file paths back to the client."""
    response = api_client.get_location("zz", "00000")
    assert response.status_code == 404
    body_text = response.text.lower()
    for leaky_token in ("traceback", "exception", "stack trace", "at java.", "at com."):
        assert leaky_token not in body_text
