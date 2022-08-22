@UI
Feature: Test basic Support Tool Functionality

  Scenario: Create a Survey, Collection Exercise and Load a Sample
    Given the support tool landing page is displayed
    And The Create Survey Button is clicked on
    And a Survey called "CreateSurveyTest" plus unique suffix is created for sample file "social_sample_3_lines_fields.csv" with sensitive columns []
    When the survey is clicked on it should display the collex page
    And the create collection exercise button is clicked on and entered in details
    And the collex is clicked on and displays the details page
    Then I click the upload sample file button with file "social_sample_3_lines_fields.csv"


  Scenario: Creating an export file template
    Given the support tool landing page is displayed
    And the Create Export File Template button is clicked on
    When an export file template with packcode "export-file-packcode" and template ["__uac__"] has been created
    Then I should see the export file template in the template list

  Scenario: Creating an Export File Action Rule
    Given the support tool landing page is displayed
    And the Create Export File Template button is clicked on
    And an export file template with packcode "export-file-packcode" and template ["__uac__"] has been created
    And I should see the export file template in the template list
    And The Create Survey Button is clicked on
    And a Survey called "ActionRuleTest" plus unique suffix is created for sample file "social_sample_3_lines_fields.csv" with sensitive columns []
    And the survey is clicked on it should display the collex page
    And the create collection exercise button is clicked on and entered in details
    And the export file template has been added to the allow on action rule list
    And the collex is clicked on and displays the details page
    And I click the upload sample file button with file "social_sample_3_lines_fields.csv"
    When I create an action rule
    Then I can see the Action Rule has been triggered and export files been created

  @reset_notify_stub
  Scenario: Creating an Email Action Rule
    Given the support tool landing page is displayed
    And the Create Email Template button is clicked on
    And an email template with packcode "email-packcode" and template ["__uac__"] has been created
    And I should see the email template in the template list
    And The Create Survey Button is clicked on
    And a Survey called "EmailTest" plus unique suffix is created for sample file "sis_survey_link.csv" with sensitive columns ["emailAddress"]
    And the survey is clicked on it should display the collex page
    And the create collection exercise button is clicked on and entered in details
    And the email template has been added to the allow on action rule list
    And the collex is clicked on and displays the details page
    And I click the upload sample file button with file "sis_survey_link.csv"
    When I create an email action rule
    Then I can see the Action Rule has been triggered and emails sent to notify api
