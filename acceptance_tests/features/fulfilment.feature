Feature: Fulfilments can be requested for a case

  Scenario: A print fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print fulfilment template has been created with template "["ADDRESS_LINE1","POSTCODE","__uac__"]" and print supplier "SUPPLIER_A"
    And a print fulfilment has been requested
    When print fulfilments are triggered to be sent for printing
    Then UAC_UPDATED messages are emitted with active set to true
    And a print file is created with correct rows
    And the events logged against the case are [SAMPLE_LOADED,PRINTED_PACK_CODE,FULFILMENT]
