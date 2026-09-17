from __future__ import annotations

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class ArticlePage(BasePage):
    ARTICLE_TITLE = (By.ID, "org.wikipedia:id/view_page_title_text")
    # The bookmark/save icon in the article's bottom toolbar. Tapping it the
    # first time saves to the default list; the "add to a specific list"
    # flow (SaveToReadingListDialog) is what this test suite exercises.
    SAVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Save page")
    SAVED_BUTTON_STATE = (AppiumBy.ACCESSIBILITY_ID, "Saved")

    def get_title(self) -> str:
        return self.wait_visible(self.ARTICLE_TITLE).text

    def open_add_to_reading_list(self):
        from src.pages.save_to_reading_list_dialog import SaveToReadingListDialog

        self.click(self.SAVE_BUTTON)
        return SaveToReadingListDialog(self.driver)

    def is_saved(self) -> bool:
        return self.is_present(self.SAVED_BUTTON_STATE)
