"""
Loads config/config.yaml once and exposes platform-scoped settings.
A --platform CLI flag (see tests/conftest.py) decides which of the
android:/ios: sections applies for a given test run.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


class ConfigReader:
    _data: dict[str, Any] | None = None

    @classmethod
    def _load(cls) -> dict[str, Any]:
        if cls._data is None:
            with open(_CONFIG_PATH, encoding="utf-8") as f:
                cls._data = yaml.safe_load(f)
        return cls._data

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return cls._load().get(key, default)

    @classmethod
    def platform_settings(cls, platform: str) -> dict[str, Any]:
        """platform is 'android' or 'ios'."""
        data = cls._load()
        if platform not in data:
            raise KeyError(f"No '{platform}:' section in config.yaml")
        return data[platform]
