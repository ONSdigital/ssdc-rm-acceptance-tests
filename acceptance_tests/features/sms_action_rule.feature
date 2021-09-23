Feature: Check action rule for SMS feature is able to send SMS via notify

  Scenario: A SMS message is sent via action rule
    Given sample file "sis_survey_link.csv" with sensitive columns [PHONE_NUMBER, CHILD_NAME] is loaded successfully
    And a sms template has been created with template "["__sensitive__.CHILD_NAME","__uac__"]"
    When a SMS action rule has been created
    Then the events logged against the case are [NEW_CASE,ACTION_RULE_SMS_REQUEST]
    And notify api was called with SMS template with phone number "07453656573000"
#    And stored events sensitive PHONE_NUMBER column is redacted
