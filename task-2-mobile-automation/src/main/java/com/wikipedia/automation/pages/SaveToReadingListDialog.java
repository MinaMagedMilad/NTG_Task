package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;

/**
 * The bottom-sheet dialog listing existing reading lists plus a
 * "Create new reading list" action, shown after ArticlePage.openAddToReadingList().
 */
public class SaveToReadingListDialog extends BasePage {

    private final By dialogTitle = By.id("org.wikipedia:id/onboarding_message");
    private final By createNewListOption = By.AccessibilityId("Create new reading list");
    private final By newListNameInput = By.id("org.wikipedia:id/text_input");
    private final By newListCreateConfirm = By.id("org.wikipedia:id/onboarding_button");
    private final By existingListItem = By.id("org.wikipedia:id/item_title");
    private final By alreadyInListIndicator = By.id("org.wikipedia:id/item_check_icon");

    public SaveToReadingListDialog(AppiumDriver driver) {
        super(driver);
    }

    /** Creates a brand-new reading list with the given name and saves the article into it. */
    public void createNewListAndSave(String listName) {
        click(createNewListOption);
        type(newListNameInput, listName);
        click(newListCreateConfirm);
    }

    /** Adds the article to an already-existing list by its display name. */
    public void addToExistingList(String listName) {
        By listByName = By.xpath("//*[@resource-id='org.wikipedia:id/item_title' and @text='" + listName + "']");
        click(listByName);
    }

    /**
     * Whether the given list is already shown as checked/containing this
     * article - used by the duplicate-prevention check so the test can
     * assert the app *shows* the article as already added rather than
     * silently creating a second entry.
     */
    public boolean isArticleAlreadyInList(String listName) {
        By checkedRowForList = By.xpath(
                "//*[@resource-id='org.wikipedia:id/item_title' and @text='" + listName + "']"
                        + "/following-sibling::*[@resource-id='org.wikipedia:id/item_check_icon']");
        return isPresent(checkedRowForList);
    }
}
