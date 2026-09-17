"""
Builds an Appium driver for either platform. Kept separate from the
pytest fixture (tests/conftest.py) so driver construction has no
dependency on pytest and could be reused from a plain script if needed.
"""
from __future__ import annotations

import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from src.config_reader import ConfigReader


def build_driver(platform: str) -> webdriver.Remote:
    platform = platform.lower()
    settings = ConfigReader.platform_settings(platform)
    server_url = ConfigReader.get("appium_server_url")

    if platform == "ios":
        options = XCUITestOptions()
        options.device_name = settings["device_name"]
        options.platform_version = settings["platform_version"]
        options.automation_name = settings["automation_name"]
        options.bundle_id = settings["bundle_id"]
        if os.path.exists(settings.get("app_path", "")):
            options.app = os.path.abspath(settings["app_path"])
    elif platform == "android":
        options = UiAutomator2Options()
        options.device_name = settings["device_name"]
        options.platform_version = settings["platform_version"]
        options.automation_name = settings["automation_name"]
        options.app_package = settings["app_package"]
        options.app_activity = settings["app_activity"]
        options.no_reset = True  # preserve app state between scenarios where useful
        if os.path.exists(settings.get("app_path", "")):
            options.app = os.path.abspath(settings["app_path"])
    else:
        raise ValueError(f"Unsupported platform '{platform}' - expected 'android' or 'ios'")

    driver = webdriver.Remote(command_executor=server_url, options=options)
    driver.implicitly_wait(ConfigReader.get("implicit_wait_seconds", 10))
    return driver
