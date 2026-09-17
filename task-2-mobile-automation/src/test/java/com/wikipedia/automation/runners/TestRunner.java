package com.wikipedia.automation.runners;

import io.cucumber.testng.AbstractTestNGCucumberTests;
import io.cucumber.testng.CucumberOptions;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;

/**
 * Cucumber-TestNG bridge. Using cucumber-testng (rather than the plain
 * JUnit runner) is what lets testng.xml drive parallel execution and
 * platform-specific suites (see testng.xml, and the README's notes on
 * running Android/iOS suites side by side).
 */
@CucumberOptions(
        features = "src/test/resources/features",
        glue = {"com.wikipedia.automation.stepdefinitions", "com.wikipedia.automation.hooks"},
        plugin = {
                "pretty",
                "html:target/cucumber-reports/cucumber.html",
                "json:target/cucumber-reports/cucumber.json",
                "io.qameta.allure.cucumber7jvm.AllureCucumber7Jvm"
        },
        monochrome = true
        // tags = "@smoke"  // uncomment to run just the smoke subset, e.g. for a fast pre-merge gate
)
public class TestRunner extends AbstractTestNGCucumberTests {

    /**
     * TestNG's <parameter name="platform"> in testng.xml is only injected
     * into @Parameters-annotated methods, not into System properties - so
     * without this, ConfigReader.platform() would silently fall back to
     * config.properties' default for every <test> block, and the two
     * "parallel" suites in testng.xml would both run Android. This bridges
     * the XML parameter into a system property before any scenario (and
     * therefore before Hooks.setUp() -> DriverManager.initDriver()) runs.
     */
    @Parameters("platform")
    @BeforeClass(alwaysRun = true)
    public void setPlatformFromSuite(@Optional("android") String platform) {
        System.setProperty("platform", platform);
    }

    @Override
    @org.testng.annotations.DataProvider(parallel = true)
    public Object[][] scenarios() {
        // Overriding to enable Cucumber's own scenario-level parallelism
        // within a single TestNG <test>, in addition to the platform-level
        // parallelism configured in testng.xml.
        return super.scenarios();
    }
}
