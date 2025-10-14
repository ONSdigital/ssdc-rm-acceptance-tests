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

  Scenario: Create an invalid survey
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey with no filed entered is attempted to be created
    Then I should see 3 problems with this page
    And I see a "Enter a survey name" error
    And I see a "Enter a sample definition URL" error
    And I see a "Select a sample template" error

  @regression
  Scenario: Edit a surveys details and removing fields
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    When the name edit link is clicked
    And fields are emptied
    Then I should see 2 problems with this page
    And I see a "Enter a survey name" error
    And I see a "Enter a sample definition URL" error

  @regression
  Scenario: Create a survey with a too long name
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey with a name longer than 255 characters is attempted to be created
    Then the name should be truncated to 255 characters

  Scenario: Create a Collection Exercise and View Details
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    When the "Add collection exercise" button is clicked
    And a collection exercise called "SupportFrontendCollexTest" plus unique suffix, with a start date of "2050-01-01" and an end date of "2050-12-31" is created
    Then I should see the new collection exercise details
    And the new collection exercise is published to pubsub

  @regression
  Scenario: Edit a Collection Exercise
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    And the "Add collection exercise" button is clicked
    And a collection exercise called "SupportFrontendCollexTest" plus unique suffix, with a start date of "2050-01-01" and an end date of "2050-12-31" is created
    When the collection exercise name edit link is clicked
    And the collection exercise name is changed to "EditedSupportFrontendCollexTest"
    Then I should see the edited collection name
    And the new collection exercise is published to pubsub
    And the edited collection exercise is published to pubsub

  Scenario: Create an invalid Collection Exercise
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    When the "Add collection exercise" button is clicked
    And a collection exercise is saved with no fields entered
    Then I should see 5 problems with this page

  @regression
  Scenario: Edit a Collection Exercise with invalid data
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendCollexTest" plus unique suffix is created
    And the "Add collection exercise" button is clicked
    And a collection exercise called "SupportFrontendCollexTest" plus unique suffix, with a start date of "2050-01-01" and an end date of "2050-12-31" is created
    And the new collection exercise is published to pubsub
    When the collection exercise name edit link is clicked
    And the collection exercise name and description is changed to an empty string
    Then I should see 2 problems with this page
