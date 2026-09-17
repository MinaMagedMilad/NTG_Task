from __future__ import annotations

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, "org.wikipedia:id/search_src_text")
    RESULTS_LIST = (By.ID, "org.wikipedia:id/search_results_list")

    def search_for(self, query: str) -> "SearchPage":
        self.type_text(self.SEARCH_INPUT, query)
        return self

    @staticmethod
    def _exact_result_locator(article_title: str):
        return (
            By.XPATH,
            f"//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='{article_title}']",
        )

    def open_result(self, article_title: str):
        from src.pages.article_page import ArticlePage  # local import avoids a circular import with ArticlePage

        self.click(self._exact_result_locator(article_title))
        return ArticlePage(self.driver)

    def has_result_matching(self, article_title: str) -> bool:
        """Waits for the results list to render, then checks for an exact title match."""
        self.wait_visible(self.RESULTS_LIST)
        return self.is_present(self._exact_result_locator(article_title))
