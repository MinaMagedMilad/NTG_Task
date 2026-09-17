package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.PointerInput;
import org.openqa.selenium.interactions.Sequence;

import java.time.Duration;
import java.util.Collections;

public class ReadingListDetailPage extends BasePage {

    private final By articleRow = By.id("org.wikipedia:id/page_list_item_title");
    private final By overflowMenuButton = By.AccessibilityId("More options");
    private final By removeFromListOption = By.AccessibilityId("Remove from this list");
    private final By emptyStateMessage = By.id("org.wikipedia:id/read_list_empty_text");

    public ReadingListDetailPage(AppiumDriver driver) {
        super(driver);
    }

    public boolean containsArticle(String articleTitle) {
        By articleByTitle = By.xpath(
                "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='" + articleTitle + "']");
        return isDisplayed(articleByTitle, Duration.ofSeconds(10));
    }

    /** Long-presses the article row to reveal its context menu, then taps "Remove from this list". */
    public void removeArticle(String articleTitle) {
        By articleByTitle = By.xpath(
                "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='" + articleTitle + "']");
        WebElement row = waitVisible(articleByTitle);
        longPress(row);
        click(removeFromListOption);
    }

    public boolean isEmpty() {
        return isPresent(emptyStateMessage) || waitAllAssertNoRows();
    }

    private boolean waitAllAssertNoRows() {
        return driver.findElements(articleRow).isEmpty();
    }

    /** W3C Actions long-press, since Appium dropped the old TouchAction API. */
    private void longPress(WebElement element) {
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence longPress = new Sequence(finger, 0);
        int x = element.getLocation().getX() + (element.getSize().getWidth() / 2);
        int y = element.getLocation().getY() + (element.getSize().getHeight() / 2);

        longPress.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), x, y));
        longPress.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        longPress.addAction(new org.openqa.selenium.interactions.Pause(finger, Duration.ofMillis(800)));
        longPress.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));

        driver.perform(Collections.singletonList(longPress));
    }
}
