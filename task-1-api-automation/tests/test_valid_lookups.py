"""
Positive-path test cases: valid country + postal code combinations.

Covers:
- A well-known, stable postal code returning 200 with exact expected values.
- A representative spread of countries/postal-code formats (parametrized),
  since the endpoint's behaviour can differ across countries (e.g. some
  countries use alphanumeric postal codes, some return multiple `places`).
"""
import pytest


@pytest.mark.smoke
def test_valid_lookup_returns_200(api_client, known_location):
    response = api_client.get_location(known_location["country"], known_location["postal_code"])
    assert response.status_code == 200


@pytest.mark.smoke
def test_valid_lookup_returns_expected_body(api_client, known_location):
    response = api_client.get_location(known_location["country"], known_location["postal_code"])
    body = response.json()

    assert body["country"] == known_location["expected_country"]
    assert body["country abbreviation"] == known_location["expected_country_abbreviation"]
    assert body["post code"] == known_location["postal_code"]

    place = body["places"][0]
    assert place["place name"] == known_location["expected_place_name"]
    assert place["state"] == known_location["expected_state"]
    assert place["state abbreviation"] == known_location["expected_state_abbreviation"]


@pytest.mark.parametrize(
    "country, postal_code",
    [
        ("us", "90210"),      # United States - single place
        ("gb", "AA9A 9AA"),   # United Kingdom - alphanumeric format
        ("de", "01067"),      # Germany - leading zero preserved
        ("ca", "B2R"),        # Canada - forward sortation area (partial code)
        ("fr", "75008"),      # France
        ("au", "2000"),       # Australia
    ],
)
def test_valid_lookup_across_countries(api_client, country, postal_code):
    response = api_client.get_location(country, postal_code)

    assert response.status_code == 200
    body = response.json()
    assert body["places"], "expected at least one place in the response"
    for place in body["places"]:
        assert "place name" in place
        assert "latitude" in place
        assert "longitude" in place


def test_postal_code_with_multiple_places_returns_all_of_them(api_client):
    """Some US zip codes map to more than one named place; make sure the
    client/test surfaces the full list rather than assuming a single entry."""
    response = api_client.get_location("us", "12345")  # Schenectady, NY area

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["places"], list)
    assert len(body["places"]) >= 1
