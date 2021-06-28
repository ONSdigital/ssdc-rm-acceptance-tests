
Feature: requesting fulfilments for a case

  Scenario: A print fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a fulfilment template has been created with template "["ADDRESS_LINE1","POSTCODE","__uac__"]" and print supplier "SUPPLIER_A"
    And a fulfilment has been requested
    When fulfilments trigger
    Then uac_updated msgs are emitted with active set to true
    And a print file is created with correct rows
