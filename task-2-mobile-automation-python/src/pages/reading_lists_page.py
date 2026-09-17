"""The "Saved" / Reading Lists tab, reached from the bottom navigation bar."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class ReadingListsPage(BasePage):
    SAVED_TAB = (AppiumBy.ACCESSIBILITY_ID, "Saved")
    SEARCH_LISTS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Search reading lists")
    SEARCH_LISTS_INPUT = (By.ID, "org.wikipedia:id/search_src_text")

    @classmethod
    def navigate_to(cls, driver) -> "ReadingListsPage":
        page = cls(driver)
        page.click(cls.SAVED_TAB)
        return page

    def search_for_list(self, list_name: str) -> "ReadingListsPage":
        self.click(self.SEARCH_LISTS_BUTTON)
        self.type_text(self.SEARCH_LISTS_INPUT, list_name)
        return self

    def is_list_visible(self, list_name: str) -> bool:
        return self.is_displayed(self._list_row_locator(list_name), timeout=10)

    def open_list(self, list_name: str):
        from src.pages.reading_list_detail_page import ReadingListDetailPage

        self.click(self._list_row_locator(list_name))
        return ReadingListDetailPage(self.driver)

    @staticmethod
    def _list_row_locator(list_name: str):
        return (By.XPATH, f"//*[@resource-id='org.wikipedia:id/item_title' and @text='{list_name}']")
