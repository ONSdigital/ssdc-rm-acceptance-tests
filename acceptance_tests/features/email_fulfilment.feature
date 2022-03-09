Feature: Email fulfilment

  @reset_notify_stub
  Scenario: An email fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an email template has been created with template "["__uac__", "__qid__"]"
    And fulfilments are authorised on email template
    When a request has been made for a replacement UAC by email from email address "foo@bar.baz"
    Then UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the email fulfilment UAC
    And the events logged against the case are ["NEW_CASE","EMAIL_FULFILMENT"]
    And notify api was called with the correct email template and values

  @reset_notify_stub
  Scenario: An email fulfilment is requested for a case with no uac/qid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an email template has been created with template "[]"
    And fulfilments are authorised on email template
    When a request has been made for a replacement UAC by email from email address "foo@bar.baz"
    Then the events logged against the case are ["NEW_CASE","EMAIL_FULFILMENT"]
    And notify api was called with the correct email template and values

  @reset_notify_stub
  Scenario: An email fulfilment is requested including personalisation
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an email template has been created with template "["__request__.name"]"
    And fulfilments are authorised on email template
    When a request has been made for a replacement UAC by email from email address "foo@bar.baz" with personalisation {"name": "Joe Bloggs"}
    Then the events logged against the case are ["NEW_CASE","EMAIL_FULFILMENT"]
    And notify api was called with the correct email template and values
