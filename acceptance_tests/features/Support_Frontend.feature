@UI @SupportFrontend
Feature: Test functionality of the Support Frontend

  @regression
  Scenario: Create a Survey and View Details
    Given the support frontend is displayed
    When the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    Then I should see the new surveys details

  Scenario: Edit a surveys details
    Given the support frontend is displayed
    And the "Create new survey" button is clicked
    And a survey called "SupportFrontendTest" plus unique suffix is created
    When the name edit link is clicked
    And the name is changed to "EditedSupportFrontendTest"
    Then I should see the edited survey name