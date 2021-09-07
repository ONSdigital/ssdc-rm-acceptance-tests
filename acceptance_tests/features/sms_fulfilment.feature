Feature: Sms fulfilment

  Scenario: A SMS fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a sms template has been created with template "["__uac__", "__qid__"]"
    And fulfilments are authorised on sms template
    When a request has been made for a replacement UAC by SMS from phone number "07123456789"
    Then UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And the events logged against the case are [NEW_CASE,SMS_FULFILMENT]
    And notify api was called with SMS template


  Scenario: A SMS fulfilment is requested for a case with no uac/qid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a sms template has been created with template "[]"
    And fulfilments are authorised on sms template
    When a request has been made for a replacement UAC by SMS from phone number "07123456789"
    Then the events logged against the case are [NEW_CASE,SMS_FULFILMENT]
    And notify api was called with SMS template