Feature: Print fulfilments can be requested for a case

  @regression
  Scenario: A print fulfilment is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for the export file template "address_line1__postcode__uac"
    And a print fulfilment has been requested
    And the events logged against the case are ["NEW_CASE","PRINT_FULFILMENT"]
    When export file fulfilments are triggered to be exported
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","PRINT_FULFILMENT"]

  Scenario: A print fulfilment including personalisation is requested for a case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for the export file template "request_name__address_line1__postcode__uac"
    And a print fulfilment with personalisation {"name":"Joe Bloggs"} has been requested
    And the events logged against the case are ["NEW_CASE","PRINT_FULFILMENT"]
    When export file fulfilments are triggered to be exported
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","PRINT_FULFILMENT"]
