package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;

public class SearchPage extends BasePage {

    private final By searchInput = By.id("org.wikipedia:id/search_src_text");
    private final By resultsList = By.id("org.wikipedia:id/search_results_list");

    public SearchPage(AppiumDriver driver) {
        super(driver);
    }

    public SearchPage searchFor(String query) {
        type(searchInput, query);
        return this;
    }

    /** Taps the first result whose title text exactly matches {@code articleTitle}. */
    public ArticlePage openResult(String articleTitle) {
        By exactResult = By.xpath(
                "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='" + articleTitle + "']");
        click(exactResult);
        return new ArticlePage(driver);
    }

    /** Waits for the results list to render, then checks for an exact title match. */
    public boolean hasResultMatching(String articleTitle) {
        waitVisible(resultsList);
        By exactResult = By.xpath(
                "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='" + articleTitle + "']");
        return isPresent(exactResult);
    }
}
