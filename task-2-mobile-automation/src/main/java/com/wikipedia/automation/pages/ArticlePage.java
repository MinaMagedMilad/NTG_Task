package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;

public class ArticlePage extends BasePage {

    private final By articleTitle = By.id("org.wikipedia:id/view_page_title_text");
    // The bookmark/save icon in the article's bottom toolbar. Tapping it the
    // first time saves to the default list; tapping again on an already
    // saved article opens/removes it. Long variants of the Wikipedia app
    // route "add to a specific list" through the overflow/bookmark-long-press
    // flow captured in SaveToReadingListDialog.
    private final By saveButton = By.AccessibilityId("Save page");
    private final By savedButtonState = By.AccessibilityId("Saved");

    public ArticlePage(AppiumDriver driver) {
        super(driver);
    }

    public String getTitle() {
        return waitVisible(articleTitle).getText();
    }

    /** Opens the "add to reading list" bottom sheet (long-press equivalent / tap-and-hold on save icon). */
    public SaveToReadingListDialog openAddToReadingList() {
        waitClickable(saveButton).click();
        return new SaveToReadingListDialog(driver);
    }

    public boolean isSaved() {
        return isPresent(savedButtonState);
    }
}
