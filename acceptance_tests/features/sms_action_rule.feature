Feature: Check action rule for SMS feature is able to send SMS via notify

  @reset_notify_stub
  Scenario: A SMS message is sent via action rule
    Given sample file "sis_survey_link.csv" with sensitive columns ["firstName","lastName","childFirstName","childMiddleNames","childLastName","childDob","mobileNumber","emailAddress","consentGivenTest","consentGivenSurvey"] is loaded successfully
    And an sms template has been created with template "sensitive_childlastname__uac"
    When a SMS action rule has been created
    Then 1 UAC_UPDATE messages are emitted with active set to true
    And the events logged against the case are ["NEW_CASE","ACTION_RULE_SMS_REQUEST","ACTION_RULE_SMS_CONFIRMATION"]
    And notify api was called with SMS template with phone number "07123456666" and child surname "McChildy"
