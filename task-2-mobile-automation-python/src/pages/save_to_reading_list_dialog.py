"""
The bottom-sheet dialog listing existing reading lists plus a
"Create new reading list" action, shown after ArticlePage.open_add_to_reading_list().
"""
from __future__ import annotations

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class SaveToReadingListDialog(BasePage):
    CREATE_NEW_LIST_OPTION = (AppiumBy.ACCESSIBILITY_ID, "Create new reading list")
    NEW_LIST_NAME_INPUT = (By.ID, "org.wikipedia:id/text_input")
    NEW_LIST_CREATE_CONFIRM = (By.ID, "org.wikipedia:id/onboarding_button")

    def create_new_list_and_save(self, list_name: str) -> None:
        """Creates a brand-new reading list with the given name and saves the article into it."""
        self.click(self.CREATE_NEW_LIST_OPTION)
        self.type_text(self.NEW_LIST_NAME_INPUT, list_name)
        self.click(self.NEW_LIST_CREATE_CONFIRM)

    def add_to_existing_list(self, list_name: str) -> None:
        """Adds the article to an already-existing list by its display name."""
        self.click(self._list_row_locator(list_name))

    def is_article_already_in_list(self, list_name: str) -> bool:
        """
        Whether the given list is already shown as checked/containing this
        article - used by the duplicate-prevention check so the test can
        assert the app *shows* the article as already added rather than
        silently creating a second entry.
        """
        checked_row_for_list = (
            By.XPATH,
            f"//*[@resource-id='org.wikipedia:id/item_title' and @text='{list_name}']"
            "/following-sibling::*[@resource-id='org.wikipedia:id/item_check_icon']",
        )
        return self.is_present(checked_row_for_list)

    @staticmethod
    def _list_row_locator(list_name: str):
        return (By.XPATH, f"//*[@resource-id='org.wikipedia:id/item_title' and @text='{list_name}']")
