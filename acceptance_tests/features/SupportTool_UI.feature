@UI
Feature: Test basic Support Tool Functionality

  Scenario: Create a Survey, Collection Exercise and Load a Sample
    Given the support tool landing page is displayed
    And the Create Survey Button is clicked on
    And a Survey called "CreateSurveyTest" plus unique suffix is created for sample file "social_sample_3_lines_fields.csv" with sensitive columns []
    When the survey is clicked on it should display the collection exercise page
    And the create collection exercise button is clicked, the details are submitted and the exercise is created
    And the collection exercise is clicked on, navigating to the selected exercise details page
    Then I click the upload sample file button with file "social_sample_3_lines_fields.csv"

  @regression
  Scenario: Create an export file template
    Given the support tool landing page is displayed
    And the Create Export File Template button is clicked on
    When an export file template with packcode "export-file-packcode" and template ["__uac__"] has been created
    Then I should see the export file template in the template list

  @regression
  Scenario: Create an Export File Action Rule
    Given the support tool landing page is displayed
    And the Create Export File Template button is clicked on
    And an export file template with packcode "export-file-packcode" and template ["__uac__"] has been created
    And I should see the export file template in the template list
    And the Create Survey Button is clicked on
    And a Survey called "ActionRuleTest" plus unique suffix is created for sample file "social_sample_3_lines_fields.csv" with sensitive columns []
    And the survey is clicked on it should display the collection exercise page
    And the create collection exercise button is clicked, the details are submitted and the exercise is created
    And the export file template has been added to the allow on action rule list
    And the collection exercise is clicked on, navigating to the selected exercise details page
    And I click the upload sample file button with file "social_sample_3_lines_fields.csv"
    When I create an action rule
    Then I can see the Action Rule has been triggered and export files have been created

  @reset_notify_stub
  Scenario Outline: Create an Email Action Rule
    Given the support tool landing page is displayed
    And the Create Email Template button is clicked on
    And an email template with packcode "email-packcode", notify service ref "<notify service ref>" and template ["__uac__"] has been created
    And I should see the email template in the template list
    And the Create Survey Button is clicked on
    And a Survey called "EmailTest" plus unique suffix is created for sample file "sis_survey_link.csv" with sensitive columns ["emailAddress"]
    And the survey is clicked on it should display the collection exercise page
    And the create collection exercise button is clicked, the details are submitted and the exercise is created
    And the email template has been added to the allow on action rule list
    And the collection exercise is clicked on, navigating to the selected exercise details page
    And I click the upload sample file button with file "sis_survey_link.csv"
    When I create an email action rule with email column "emailAddress"
    Then I can see the Action Rule has been triggered and emails sent to notify api with email column "emailAddress"
    And the correct number of UAC_UPDATE messages are emitted with active set to true

    @regression
    Examples:
      | notify service ref                         |
      | Office_for_National_Statistics_surveys_NHS |
      | test_service                               |

  @reset_notify_stub
  Scenario Outline: Support tool displays action rules with correct timezone
    Given the support tool landing page is displayed
    And the Create Email Template button is clicked on
    And an email template with packcode "email-packcode", notify service ref "<notify service ref>" and template ["__uac__"] has been created
    And I should see the email template in the template list
    And the Create Survey Button is clicked on
    And a Survey called "EmailTest" plus unique suffix is created for sample file "sis_survey_link.csv" with sensitive columns ["emailAddress"]
    And the survey is clicked on it should display the collection exercise page
    And the create collection exercise button is clicked, the details are submitted and the exercise is created
    And the email template has been added to the allow on action rule list
    And the collection exercise is clicked on, navigating to the selected exercise details page
    When I create an email action rule on the date "<action rule date>" with email column "emailAddress"
    Then I can see the action rule has been created in "<expected timezone>"

    @regression
    Examples:
      | notify service ref                         | action rule date | expected timezone |
      | Office_for_National_Statistics_surveys_NHS | 01-01-2124       | GMT               |
      | test_service                               | 06-06-2124       | BST               |