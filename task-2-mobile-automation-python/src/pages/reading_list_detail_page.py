from __future__ import annotations

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput

from src.pages.base_page import BasePage


class ReadingListDetailPage(BasePage):
    ARTICLE_ROW = (By.ID, "org.wikipedia:id/page_list_item_title")
    REMOVE_FROM_LIST_OPTION = (AppiumBy.ACCESSIBILITY_ID, "Remove from this list")
    EMPTY_STATE_MESSAGE = (By.ID, "org.wikipedia:id/read_list_empty_text")

    def contains_article(self, article_title: str) -> bool:
        return self.is_displayed(self._article_row_locator(article_title), timeout=10)

    def remove_article(self, article_title: str) -> None:
        """Long-presses the article row to reveal its context menu, then taps "Remove from this list"."""
        row = self.wait_visible(self._article_row_locator(article_title))
        self._long_press(row)
        self.click(self.REMOVE_FROM_LIST_OPTION)

    def is_empty(self) -> bool:
        return self.is_present(self.EMPTY_STATE_MESSAGE) or len(self.driver.find_elements(*self.ARTICLE_ROW)) == 0

    @staticmethod
    def _article_row_locator(article_title: str):
        return (
            By.XPATH,
            f"//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='{article_title}']",
        )

    def _long_press(self, element, hold_seconds: float = 0.8) -> None:
        """W3C Actions long-press, since Appium dropped the old TouchAction API."""
        finger = PointerInput(POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger, duration=250)
        location = element.location
        size = element.size
        x = location["x"] + size["width"] // 2
        y = location["y"] + size["height"] // 2

        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(hold_seconds)
        actions.pointer_action.release()
        actions.perform()
