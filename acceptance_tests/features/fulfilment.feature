Feature: Fulfilments can be requested for a case

  Scenario: A print fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["ADDRESS_LINE1","POSTCODE","__uac__"]"
    And fulfilments are authorised on print template
    And a print fulfilment has been requested
    When print fulfilments are triggered to be sent for printing
    Then UAC_UPDATED messages are emitted with active set to true
    And a print file is created with correct rows
    And the events logged against the case are [CASE_CREATED,PRINTED_PACK_CODE,FULFILMENT]


  Scenario: A SMS fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a sms template has been created with template "["__uac__", "__qid__"]"
    And fulfilments are authorised on sms template
    When a request has been made for a replacement UAC by SMS
    Then UAC_UPDATED messages are emitted with active set to true
    And the events logged against the case are [CASE_CREATED,SMS_FULFILMENT]
    And notify api was called with SMS template for fulfilment code