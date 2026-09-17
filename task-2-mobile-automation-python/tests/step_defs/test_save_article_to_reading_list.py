"""
Glue code translating the Gherkin steps in
features/save_article_to_reading_list.feature into page-object calls.

pytest-bdd auto-discovers scenarios from the .feature file (including
expanding the Scenario Outline's Examples table into one parametrized
test per row) - see scenarios() below.
"""
from __future__ import annotations

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.pages.main_page import MainPage

scenarios("../../features/save_article_to_reading_list.feature")


@pytest.fixture
def context():
    """Per-scenario mutable state, threaded through step functions via
    pytest-bdd's fixture injection instead of instance attributes (the
    class-based approach the Java/Cucumber version uses)."""
    return {}


@given("the Wikipedia app is launched")
def app_is_launched(driver, context):
    context["main_page"] = MainPage(driver)
    context["main_page"].dismiss_onboarding_if_present()
    assert context["main_page"].is_loaded(), "Expected the Explore feed to load after launch"


@when(parsers.parse('I search for the article "{article}"'))
def search_for_article(context, article):
    context["last_searched_article"] = article
    context["search_page"] = context["main_page"].open_search().search_for(article)
    assert context["search_page"].has_result_matching(article), f'Expected a search result matching "{article}"'


@when("I open the article from the search results")
def open_article_from_results(context):
    article = context["last_searched_article"]
    context["article_page"] = context["search_page"].open_result(article)


@then(parsers.parse('the article page for "{article}" should be displayed'))
def article_page_displayed(context, article):
    assert context["article_page"].get_title() == article


@when(parsers.parse('I save the article to a new reading list named "{list_name}"'))
def save_to_new_list(context, list_name):
    dialog = context["article_page"].open_add_to_reading_list()
    dialog.create_new_list_and_save(list_name)


@when("I navigate to the Reading Lists section")
def navigate_to_reading_lists(context, driver):
    from src.pages.reading_lists_page import ReadingListsPage

    context["reading_lists_page"] = ReadingListsPage.navigate_to(driver)


@when(parsers.parse('I search for the reading list "{list_name}"'))
def search_for_reading_list(context, list_name):
    context["reading_lists_page"].search_for_list(list_name)


@then(parsers.parse('the reading list "{list_name}" should be visible'))
def reading_list_visible(context, list_name):
    assert context["reading_lists_page"].is_list_visible(list_name), f'Expected reading list "{list_name}" to be visible'


@when(parsers.parse('I open the reading list "{list_name}"'))
def open_reading_list(context, list_name):
    context["reading_list_detail_page"] = context["reading_lists_page"].open_list(list_name)


@then(parsers.parse('the article "{article}" should be displayed in the reading list'))
def article_displayed_in_list(context, article):
    assert context["reading_list_detail_page"].contains_article(article), f'Expected "{article}" to appear in the reading list'


@when(parsers.parse('I remove the article "{article}" from the reading list'))
def remove_article_from_list(context, article):
    context["reading_list_detail_page"].remove_article(article)


@then(parsers.parse('the article "{article}" should no longer be in the reading list'))
def article_no_longer_in_list(context, article):
    assert not context["reading_list_detail_page"].contains_article(article), \
        f'Expected "{article}" to have been removed from the reading list'


# --- duplicate-prevention scenario ---

@when(parsers.parse('I go back to the article "{article}" and try to add it to "{list_name}" again'))
def reopen_article_and_try_add_again(context, driver, article, list_name):
    driver.back()  # out of the reading list detail screen
    driver.back()  # out of the reading lists section
    context["search_page"] = context["main_page"].open_search().search_for(article)
    context["article_page"] = context["search_page"].open_result(article)
    context["duplicate_check_dialog"] = context["article_page"].open_add_to_reading_list()


@then(parsers.parse('the app should indicate the article is already in "{list_name}"'))
def app_indicates_already_in_list(context, list_name):
    assert context["duplicate_check_dialog"].is_article_already_in_list(list_name), \
        f'Expected the "{list_name}" row to be shown as already containing this article'


@then(parsers.parse('the reading list "{list_name}" should contain the article "{article}" only once'))
def list_contains_article_exactly_once(context, driver, list_name, article):
    from src.pages.reading_lists_page import ReadingListsPage
    from selenium.webdriver.common.by import By

    context["reading_lists_page"] = ReadingListsPage.navigate_to(driver)
    context["reading_list_detail_page"] = context["reading_lists_page"].open_list(list_name)
    occurrences = len(driver.find_elements(
        By.XPATH,
        f"//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='{article}']",
    ))
    assert occurrences == 1, f'Expected exactly one entry for "{article}" in "{list_name}", found {occurrences}'
