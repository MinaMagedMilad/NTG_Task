"""Shared pytest fixtures for the Zippopotam.us API test suite."""
import sys
from pathlib import Path

import pytest

# Make `src` importable without packaging the project.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.zippopotam_client import ZippopotamClient  # noqa: E402


@pytest.fixture(scope="session")
def api_client() -> ZippopotamClient:
    client = ZippopotamClient()
    yield client
    client.close()


@pytest.fixture
def known_location():
    """A postal code whose response body is stable and well documented,
    used for exact-value assertions rather than just shape checks."""
    return {
        "country": "us",
        "postal_code": "90210",
        "expected_country": "United States",
        "expected_country_abbreviation": "US",
        "expected_place_name": "Beverly Hills",
        "expected_state": "California",
        "expected_state_abbreviation": "CA",
    }
