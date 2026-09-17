package com.wikipedia.automation.stepdefinitions;

import com.wikipedia.automation.driver.DriverManager;
import com.wikipedia.automation.pages.*;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.testng.Assert;

/**
 * Glue code translating the Gherkin steps in
 * save_article_to_reading_list.feature into page-object calls.
 *
 * Page objects are held as instance fields rather than statics: Cucumber
 * instantiates one step-definition object per scenario, which is what
 * keeps scenarios independent under parallel execution (see testng.xml).
 */
public class ReadingListStepDefinitions {

    private MainPage mainPage;
    private SearchPage searchPage;
    private ArticlePage articlePage;
    private ReadingListsPage readingListsPage;
    private ReadingListDetailPage readingListDetailPage;
    private SaveToReadingListDialog dialogForDuplicateCheck;
    private String lastSearchedArticle;

    @Given("the Wikipedia app is launched")
    public void the_wikipedia_app_is_launched() {
        mainPage = new MainPage(DriverManager.getDriver());
        mainPage.dismissOnboardingIfPresent();
        Assert.assertTrue(mainPage.isLoaded(), "Expected the Explore feed to load after launch");
    }

    @When("I search for the article {string}")
    public void i_search_for_the_article(String article) {
        lastSearchedArticle = article;
        searchPage = mainPage.openSearch().searchFor(article);
        Assert.assertTrue(searchPage.hasResultMatching(article),
                "Expected a search result matching \"" + article + "\"");
    }

    @And("I open the article from the search results")
    public void i_open_the_article_from_the_search_results() {
        // The article title is reused from the last search step via the
        // scenario's own data table (Scenario Outline substitutes it into
        // this step's neighbouring steps), so we re-derive it from the
        // currently visible page instead of threading extra state through.
        articlePage = searchPage.openResult(lastSearchedArticle);
    }

    @Then("the article page for {string} should be displayed")
    public void the_article_page_for_should_be_displayed(String article) {
        Assert.assertEquals(articlePage.getTitle(), article);
    }

    @When("I save the article to a new reading list named {string}")
    public void i_save_the_article_to_a_new_reading_list_named(String listName) {
        SaveToReadingListDialog dialog = articlePage.openAddToReadingList();
        dialog.createNewListAndSave(listName);
    }

    @And("I navigate to the Reading Lists section")
    public void i_navigate_to_the_reading_lists_section() {
        readingListsPage = ReadingListsPage.navigateTo(DriverManager.getDriver());
    }

    @And("I search for the reading list {string}")
    public void i_search_for_the_reading_list(String listName) {
        readingListsPage.searchForList(listName);
    }

    @Then("the reading list {string} should be visible")
    public void the_reading_list_should_be_visible(String listName) {
        Assert.assertTrue(readingListsPage.isListVisible(listName),
                "Expected reading list \"" + listName + "\" to be visible");
    }

    @When("I open the reading list {string}")
    public void i_open_the_reading_list(String listName) {
        readingListDetailPage = readingListsPage.openList(listName);
    }

    @Then("the article {string} should be displayed in the reading list")
    public void the_article_should_be_displayed_in_the_reading_list(String article) {
        Assert.assertTrue(readingListDetailPage.containsArticle(article),
                "Expected \"" + article + "\" to appear in the reading list");
    }

    @When("I remove the article {string} from the reading list")
    public void i_remove_the_article_from_the_reading_list(String article) {
        readingListDetailPage.removeArticle(article);
    }

    @Then("the article {string} should no longer be in the reading list")
    public void the_article_should_no_longer_be_in_the_reading_list(String article) {
        Assert.assertFalse(readingListDetailPage.containsArticle(article),
                "Expected \"" + article + "\" to have been removed from the reading list");
    }

    // --- duplicate-prevention scenario ---

    @When("I go back to the article {string} and try to add it to {string} again")
    public void i_go_back_to_the_article_and_try_to_add_it_to_again(String article, String listName) {
        DriverManager.getDriver().navigate().back(); // back out of the reading list detail screen
        DriverManager.getDriver().navigate().back(); // back out of the reading lists section
        searchPage = mainPage.openSearch().searchFor(article);
        articlePage = searchPage.openResult(article);
        this.dialogForDuplicateCheck = articlePage.openAddToReadingList();
    }

    @Then("the app should indicate the article is already in {string}")
    public void the_app_should_indicate_the_article_is_already_in(String listName) {
        Assert.assertTrue(dialogForDuplicateCheck.isArticleAlreadyInList(listName),
                "Expected the \"" + listName + "\" row to be shown as already containing this article");
    }

    @And("the reading list {string} should contain the article {string} only once")
    public void the_reading_list_should_contain_the_article_only_once(String listName, String article) {
        readingListsPage = ReadingListsPage.navigateTo(DriverManager.getDriver());
        readingListDetailPage = readingListsPage.openList(listName);
        long occurrences = DriverManager.getDriver()
                .findElements(org.openqa.selenium.By.xpath(
                        "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='" + article + "']"))
                .size();
        Assert.assertEquals(occurrences, 1, "Expected exactly one entry for \"" + article + "\" in \"" + listName + "\"");
    }
}
