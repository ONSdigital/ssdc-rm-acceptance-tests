Feature: Print fulfilments can be requested for a case

  Scenario: A print fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "["ADDRESS_LINE1","POSTCODE","__uac__"]"
    And fulfilments are authorised on the export file template
    And a print fulfilment has been requested
    And the events logged against the case are ["NEW_CASE","PRINT_FULFILMENT"]
    When export file fulfilments are triggered to be exported
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","PRINT_FULFILMENT"]

  Scenario: A print fulfilment including personalisation is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "["__request__.name","ADDRESS_LINE1","POSTCODE","__uac__"]"
    And fulfilments are authorised on the export file template
    And a print fulfilment with personalisation {"name":"Joe Bloggs"} has been requested
    And the events logged against the case are ["NEW_CASE","PRINT_FULFILMENT"]
    When export file fulfilments are triggered to be exported
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","PRINT_FULFILMENT"]
