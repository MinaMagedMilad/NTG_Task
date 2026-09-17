"""Common wait/interaction helpers shared by every page object."""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get("explicit_wait_seconds", 20))

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_all_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.wait_clickable(locator).click()

    def type_text(self, locator, text: str):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)

    def is_displayed(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_present(self, locator) -> bool:
        return len(self.driver.find_elements(*locator)) > 0
