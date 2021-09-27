Feature: Check action rule for SMS feature is able to send SMS via notify

  @reset_notify_stub
  Scenario: A SMS message is sent via action rule
    Given sample file "sis_survey_link.csv" with sensitive columns [PHONE_NUMBER,CHILD_NAME] is loaded successfully
    And a sms template has been created with template "["__sensitive__.CHILD_NAME","__uac__"]"
    When a SMS action rule has been created
    Then the events logged against the case are [NEW_CASE,ACTION_RULE_SMS_REQUEST,SMS_FULFILMENT]
    And notify api was called with SMS template with phone number "07123456789" and Childs name "Huckleberry Finn"
