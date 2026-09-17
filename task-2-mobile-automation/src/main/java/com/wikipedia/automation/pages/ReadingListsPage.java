package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;

/**
 * The "Saved" / Reading Lists tab, reached from the bottom navigation bar.
 * Shows every reading list the user has created.
 */
public class ReadingListsPage extends BasePage {

    private final By savedTab = By.AccessibilityId("Saved");
    private final By searchListsButton = By.AccessibilityId("Search reading lists");
    private final By searchListsInput = By.id("org.wikipedia:id/search_src_text");
    private final By listNameCell = By.id("org.wikipedia:id/item_title");

    public ReadingListsPage(AppiumDriver driver) {
        super(driver);
    }

    public static ReadingListsPage navigateTo(AppiumDriver driver) {
        ReadingListsPage page = new ReadingListsPage(driver);
        page.click(page.savedTab);
        return page;
    }

    public ReadingListsPage searchForList(String listName) {
        click(searchListsButton);
        type(searchListsInput, listName);
        return this;
    }

    public boolean isListVisible(String listName) {
        By listByName = By.xpath("//*[@resource-id='org.wikipedia:id/item_title' and @text='" + listName + "']");
        return isDisplayed(listByName, java.time.Duration.ofSeconds(10));
    }

    public ReadingListDetailPage openList(String listName) {
        By listByName = By.xpath("//*[@resource-id='org.wikipedia:id/item_title' and @text='" + listName + "']");
        click(listByName);
        return new ReadingListDetailPage(driver);
    }
}
