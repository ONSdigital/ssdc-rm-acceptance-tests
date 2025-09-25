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