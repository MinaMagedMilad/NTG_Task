"""
Thin HTTP client wrapper around the Zippopotam.us API.

Keeping request-building in one place means the test modules stay
focused on assertions rather than URL construction / session handling,
and gives a single spot to add retries, timeouts, or logging later
without touching every test.
"""
from __future__ import annotations

import requests


class ZippopotamClient:
    """Minimal client for https://api.zippopotam.us

    URL structure: api.zippopotam.us/<country>/<postal-code>
    """

    def __init__(self, base_url: str = "https://api.zippopotam.us", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get_location(self, country: str, postal_code: str) -> requests.Response:
        """GET /<country>/<postal_code>

        Returns the raw Response (not .json()) so tests can assert on
        status code, headers, and body independently, and a non-2xx
        response doesn't raise before the test gets to assert on it.
        """
        url = f"{self.base_url}/{country}/{postal_code}"
        return self.session.get(url, timeout=self.timeout)

    def close(self) -> None:
        self.session.close()
