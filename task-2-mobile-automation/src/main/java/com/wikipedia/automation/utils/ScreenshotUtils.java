package com.wikipedia.automation.utils;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

public final class ScreenshotUtils {

    private static final Path SCREENSHOT_DIR = Paths.get("target", "screenshots");

    private ScreenshotUtils() {
    }

    /** Captures a PNG screenshot and returns its bytes, for attaching directly to Allure/Extent. */
    public static byte[] captureAsBytes(AppiumDriver driver) {
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }

    /** Also writes the screenshot to target/screenshots/<name>-<timestamp>.png for local debugging. */
    public static String captureToFile(AppiumDriver driver, String scenarioName) {
        try {
            Files.createDirectories(SCREENSHOT_DIR);
            String safeName = scenarioName.replaceAll("[^a-zA-Z0-9-_]", "_");
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss"));
            Path target = SCREENSHOT_DIR.resolve(safeName + "-" + timestamp + ".png");

            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            Files.copy(src.toPath(), target);
            return target.toAbsolutePath().toString();
        } catch (IOException e) {
            // A screenshot failure shouldn't mask the original test failure.
            return "screenshot-capture-failed: " + e.getMessage();
        }
    }
}
