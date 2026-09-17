package com.wikipedia.automation.hooks;

import com.wikipedia.automation.driver.DriverManager;
import com.wikipedia.automation.utils.ScreenshotUtils;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import io.qameta.allure.Allure;

import java.io.ByteArrayInputStream;

public class Hooks {

    @Before
    public void setUp() {
        DriverManager.initDriver();
    }

    @After
    public void tearDown(Scenario scenario) {
        try {
            if (scenario.isFailed()) {
                byte[] screenshot = ScreenshotUtils.captureAsBytes(DriverManager.getDriver());

                // Attach to both the Cucumber report...
                scenario.attach(screenshot, "image/png", scenario.getName());
                // ...and to Allure, so it shows up inline on the failed step there too.
                Allure.addAttachment("Failure screenshot", new ByteArrayInputStream(screenshot));

                // Also drop a copy on disk for quick local debugging without opening a report.
                String path = ScreenshotUtils.captureToFile(DriverManager.getDriver(), scenario.getName());
                scenario.log("Screenshot saved to: " + path);
            }
        } finally {
            DriverManager.quitDriver();
        }
    }
}
