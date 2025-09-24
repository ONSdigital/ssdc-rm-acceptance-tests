@UI @SupportFrontend
Feature: Test functionality of the Support Frontend

  Scenario: Create a Survey and View Details
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    Then I should see the new surveys details

  @regression
  Scenario: Edit a surveys details
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    When the name edit link is clicked
    And the name is changed to "EditedSupportFrontendTest"
    Then I should see the edited survey name

  Scenario: Create a Collection Exercise and View Details
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    And the "Add collection exercise" button is clicked
    And a collection exercise called "SupportFrontendCollexTest" plus unique suffix, with a start date of "2050-01-01" and an end date of "2050-12-31" is created
    Then I should see the new collection exercise details
    And the new collection exercise is emitted

  @regression
  Scenario: Edit a Collection Exercise
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    And the "Add collection exercise" button is clicked
    And a collection exercise called "SupportFrontendCollexTest" plus unique suffix, with a start date of "2050-01-01" and an end date of "2050-12-31" is created
    And the collection exercise name edit link is clicked
    And the collection exercise name is changed to "EditedSupportFrontendCollexTest"
    Then I should see the edited collection name
    And the new collection exercise is emitted
    And the edited collection exercise is emitted