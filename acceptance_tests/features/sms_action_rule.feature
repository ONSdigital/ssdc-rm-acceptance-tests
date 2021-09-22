Feature: Check action rule for SMS feature is able to send SMS via notify

  Scenario: A SMS message is sent via action rule
    Given sample file "sensitive_data_sample.csv" is loaded successfully
    And a sms template has been created with template "[]"
    When a SMS action rule has been created
    Then the events logged against the case are [NEW_CASE,ACTION_RULE_SMS_REQUEST]
    And notify api was called with SMS template
