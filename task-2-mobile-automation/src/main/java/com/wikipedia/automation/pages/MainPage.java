package com.wikipedia.automation.pages;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.By;

/**
 * The app's landing "Explore" feed - the entry point after launch (and
 * after dismissing onboarding, if shown on a fresh install).
 *
 * NOTE ON LOCATORS: these accessibility-id / resource-id values follow
 * org.wikipedia's known naming conventions but have not been verified
 * against a live build in this environment (no device/emulator or
 * Appium server is available here). Before running for real, open
 * Appium Inspector against the running app and confirm/adjust each
 * locator - that's flagged again in the top-level README.
 */
public class MainPage extends BasePage {

    private final By searchTab = By.AccessibilityId("Search Wikipedia");
    private final By skipOnboardingButton = By.id("org.wikipedia:id/fragment_onboarding_skip_button");
    private final By explorFeed = By.id("org.wikipedia:id/fragment_feed_feed");

    public MainPage(AppiumDriver driver) {
        super(driver);
    }

    /** Fresh installs show a multi-page onboarding flow; no-op if it's not present. */
    public MainPage dismissOnboardingIfPresent() {
        if (isDisplayed(skipOnboardingButton, java.time.Duration.ofSeconds(5))) {
            click(skipOnboardingButton);
        }
        return this;
    }

    public SearchPage openSearch() {
        click(searchTab);
        return new SearchPage(driver);
    }

    public boolean isLoaded() {
        return isDisplayed(explorFeed, java.time.Duration.ofSeconds(10)) || isDisplayed(searchTab, java.time.Duration.ofSeconds(10));
    }
}
