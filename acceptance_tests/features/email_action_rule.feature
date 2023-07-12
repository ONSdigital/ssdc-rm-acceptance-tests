Feature: Check action rule for email feature is able to send email via notify

  @reset_notify_stub
  Scenario: An email is sent via action rule
    Given sample file "sis_survey_link.csv" with sensitive columns ["firstName","lastName","childFirstName","childMiddleNames","childLastName","childDob","mobileNumber","emailAddress","consentGivenTest","consentGivenSurvey"] is loaded successfully
    And an email template has been created with template "sensitive_childlastname__uac"
    When an email action rule has been created
    Then 1 UAC_UPDATE messages are emitted with active set to true
    And the events logged against the case are ["NEW_CASE","ACTION_RULE_EMAIL_REQUEST","ACTION_RULE_EMAIL_CONFIRMATION"]
    And notify api was called with email template with email address "nope@nope.nope" and child surname "McChildy"
