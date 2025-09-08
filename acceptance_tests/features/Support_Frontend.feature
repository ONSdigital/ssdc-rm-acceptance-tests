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
    Then I should see error messages

  @regression
  Scenario: Edit a surveys details and removing fields
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    When the name edit link is clicked
    And fields are emptied
    Then I should see error messages other than for sample template

  @regression
  Scenario: Create a survey with a too long name
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey with a name longer than 255 characters is attempted to be created
    Then the name should be truncated to 255 characters