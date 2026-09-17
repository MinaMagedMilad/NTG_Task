package com.wikipedia.automation.config;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Loads config/config.properties once and exposes typed accessors.
 * A -D system property of the same key always wins over the file, so
 * CI can override platform/device without editing tracked files, e.g.:
 * {@code mvn test -Dplatform=ios}
 */
public final class ConfigReader {

    private static final Properties PROPERTIES = new Properties();
    private static final String CONFIG_PATH = "config/config.properties";

    static {
        try (InputStream in = new FileInputStream(CONFIG_PATH)) {
            PROPERTIES.load(in);
        } catch (IOException e) {
            throw new RuntimeException("Could not load " + CONFIG_PATH + " - is it present at the project root?", e);
        }
    }

    private ConfigReader() {
    }

    public static String get(String key) {
        String override = System.getProperty(key);
        if (override != null && !override.isEmpty()) {
            return override;
        }
        String value = PROPERTIES.getProperty(key);
        if (value == null) {
            throw new RuntimeException("Missing config key: " + key);
        }
        return value;
    }

    public static String get(String key, String defaultValue) {
        String override = System.getProperty(key);
        if (override != null && !override.isEmpty()) {
            return override;
        }
        return PROPERTIES.getProperty(key, defaultValue);
    }

    public static int getInt(String key) {
        return Integer.parseInt(get(key));
    }

    public static String platform() {
        return get("platform").toLowerCase();
    }
}
