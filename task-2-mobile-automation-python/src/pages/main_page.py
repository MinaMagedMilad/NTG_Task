"""
The app's landing "Explore" feed - the entry point after launch (and
after dismissing onboarding, if shown on a fresh install).

NOTE ON LOCATORS: these accessibility-id / resource-id values follow
org.wikipedia's known naming conventions but have not been verified
against a live build in this environment (no device/emulator or
Appium server is available here). Before running for real, open
Appium Inspector against the running app and confirm/adjust each
locator - flagged again in the top-level README.
"""
from __future__ import annotations

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.search_page import SearchPage


class MainPage(BasePage):
    SEARCH_TAB = (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")
    SKIP_ONBOARDING_BUTTON = (By.ID, "org.wikipedia:id/fragment_onboarding_skip_button")
    EXPLORE_FEED = (By.ID, "org.wikipedia:id/fragment_feed_feed")

    def dismiss_onboarding_if_present(self) -> "MainPage":
        """Fresh installs show a multi-page onboarding flow; no-op if it's not present."""
        if self.is_displayed(self.SKIP_ONBOARDING_BUTTON, timeout=5):
            self.click(self.SKIP_ONBOARDING_BUTTON)
        return self

    def open_search(self) -> SearchPage:
        self.click(self.SEARCH_TAB)
        return SearchPage(self.driver)

    def is_loaded(self) -> bool:
        return self.is_displayed(self.EXPLORE_FEED, timeout=10) or self.is_displayed(self.SEARCH_TAB, timeout=10)
