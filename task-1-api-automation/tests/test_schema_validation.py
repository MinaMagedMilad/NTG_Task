"""
Contract/schema tests. Status code + spot-checked fields tell you the
happy path works; schema validation tells you the *shape* of the
response stays a stable contract (correct types, required keys present)
even for postal codes we haven't hand-picked expected values for. This
is what would actually catch a backend regression that renames a field
or changes `places` from a list to an object.
"""
import jsonschema
import pytest

LOCATION_SCHEMA = {
    "type": "object",
    "required": ["post code", "country", "country abbreviation", "places"],
    "properties": {
        "post code": {"type": "string"},
        "country": {"type": "string"},
        "country abbreviation": {"type": "string"},
        "places": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["place name", "longitude", "latitude"],
                "properties": {
                    "place name": {"type": "string"},
                    "longitude": {"type": "string"},
                    "latitude": {"type": "string"},
                    "state": {"type": "string"},
                    "state abbreviation": {"type": "string"},
                },
            },
        },
    },
}


@pytest.mark.parametrize("country, postal_code", [("us", "90210"), ("de", "10115"), ("gb", "SW1A 1AA")])
def test_response_matches_schema(api_client, country, postal_code):
    response = api_client.get_location(country, postal_code)
    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=LOCATION_SCHEMA)


def test_content_type_header_is_json(api_client, known_location):
    response = api_client.get_location(known_location["country"], known_location["postal_code"])
    assert "application/json" in response.headers.get("Content-Type", "")


def test_latitude_and_longitude_are_numeric_strings(api_client, known_location):
    """The API returns lat/long as strings; verify they're at least
    parseable as floats so a consumer can safely cast them."""
    response = api_client.get_location(known_location["country"], known_location["postal_code"])
    place = response.json()["places"][0]

    float(place["latitude"])
    float(place["longitude"])
