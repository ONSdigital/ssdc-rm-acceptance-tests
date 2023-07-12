Feature: Sms fulfilment

  @reset_notify_stub
  Scenario: A SMS fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for sms template "uac__qid"
    When a request has been made for a replacement UAC by SMS from phone number "07123456789"
    Then UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And the events logged against the case are ["NEW_CASE","SMS_FULFILMENT"]
    And notify api was called with the correct SMS template and values

  @reset_notify_stub
  @regression
  Scenario: A SMS fulfilment is requested for a case with no uac/qid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for sms template "empty"
    When a request has been made for a replacement UAC by SMS from phone number "07123456789"
    Then the events logged against the case are ["NEW_CASE","SMS_FULFILMENT"]
    And notify api was called with the correct SMS template and values

  @reset_notify_stub
  @regression
  Scenario: A SMS fulfilment is requested including personalisation
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for sms template "request_name"
    When a request has been made for a replacement UAC by SMS from phone number "07123456789" with personalisation {"name": "Joe Bloggs"}
    Then the events logged against the case are ["NEW_CASE","SMS_FULFILMENT"]
    And notify api was called with the correct SMS template and values