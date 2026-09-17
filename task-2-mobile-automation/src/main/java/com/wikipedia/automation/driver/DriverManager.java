package com.wikipedia.automation.driver;

import com.wikipedia.automation.config.ConfigReader;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.ios.options.XCUITestOptions;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

/**
 * Owns AppiumDriver creation/teardown per test thread, so parallel
 * execution (see testng.xml, parallel="tests") gets an isolated driver
 * instance per thread rather than a shared/static one that would race.
 */
public final class DriverManager {

    private static final ThreadLocal<AppiumDriver> DRIVER = new ThreadLocal<>();

    private DriverManager() {
    }

    public static AppiumDriver getDriver() {
        AppiumDriver driver = DRIVER.get();
        if (driver == null) {
            throw new IllegalStateException("Driver not initialised for this thread - call initDriver() first (see Hooks).");
        }
        return driver;
    }

    public static void initDriver() {
        String platform = ConfigReader.platform();
        try {
            URL serverUrl = new URL(ConfigReader.get("appium.server.url"));
            AppiumDriver driver = "ios".equals(platform)
                    ? new IOSDriver(serverUrl, buildIosOptions())
                    : new AndroidDriver(serverUrl, buildAndroidOptions());

            driver.manage().timeouts().implicitlyWait(
                    Duration.ofSeconds(ConfigReader.getInt("implicit.wait.seconds")));
            DRIVER.set(driver);
        } catch (MalformedURLException e) {
            throw new RuntimeException("Invalid Appium server URL in config.properties", e);
        }
    }

    private static UiAutomator2Options buildAndroidOptions() {
        UiAutomator2Options options = new UiAutomator2Options();
        options.setDeviceName(ConfigReader.get("android.deviceName"));
        options.setPlatformVersion(ConfigReader.get("android.platformVersion"));
        options.setAutomationName(ConfigReader.get("android.automationName"));
        options.setAppPackage(ConfigReader.get("android.appPackage"));
        options.setAppActivity(ConfigReader.get("android.appActivity"));

        File appFile = new File(ConfigReader.get("android.appPath"));
        if (appFile.exists()) {
            // Fresh install from APK if one is present at the configured path.
            options.setApp(appFile.getAbsolutePath());
        }
        // If no APK is provided, appPackage/appActivity alone will attach to
        // an already-installed build on the device/emulator.
        options.setNoReset(true); // preserve app state (e.g. logged-in session) between scenarios where useful
        return options;
    }

    private static XCUITestOptions buildIosOptions() {
        XCUITestOptions options = new XCUITestOptions();
        options.setDeviceName(ConfigReader.get("ios.deviceName"));
        options.setPlatformVersion(ConfigReader.get("ios.platformVersion"));
        options.setAutomationName(ConfigReader.get("ios.automationName"));
        options.setBundleId(ConfigReader.get("ios.bundleId"));

        File appFile = new File(ConfigReader.get("ios.appPath"));
        if (appFile.exists()) {
            options.setApp(appFile.getAbsolutePath());
        }
        return options;
    }

    public static void quitDriver() {
        AppiumDriver driver = DRIVER.get();
        if (driver != null) {
            driver.quit();
            DRIVER.remove();
        }
    }
}
