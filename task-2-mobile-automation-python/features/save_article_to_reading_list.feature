Feature: Save an article to a reading list
  As a Wikipedia app user
  I want to save articles into a reading list
  So that I can find them again later

  Background:
    Given the Wikipedia app is launched

  @smoke @data-driven
  Scenario Outline: Save an article to a new reading list, then remove it
    When I search for the article "<article>"
    And I open the article from the search results
    Then the article page for "<article>" should be displayed
    When I save the article to a new reading list named "<listName>"
    And I navigate to the Reading Lists section
    And I search for the reading list "<listName>"
    Then the reading list "<listName>" should be visible
    When I open the reading list "<listName>"
    Then the article "<article>" should be displayed in the reading list
    When I remove the article "<article>" from the reading list
    Then the article "<article>" should no longer be in the reading list

    Examples:
      | article               | listName          |
      | Artificial intelligence | AI Reading List  |
      | Software testing        | QA Reading List  |

  @regression
  Scenario: An article cannot be duplicated in the same reading list
    When I search for the article "Artificial intelligence"
    And I open the article from the search results
    And I save the article to a new reading list named "No Duplicates List"
    And I navigate to the Reading Lists section
    And I search for the reading list "No Duplicates List"
    And I open the reading list "No Duplicates List"
    Then the article "Artificial intelligence" should be displayed in the reading list
    When I go back to the article "Artificial intelligence" and try to add it to "No Duplicates List" again
    Then the app should indicate the article is already in "No Duplicates List"
    And the reading list "No Duplicates List" should contain the article "Artificial intelligence" only once
