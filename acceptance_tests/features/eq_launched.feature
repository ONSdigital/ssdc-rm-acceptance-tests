Feature: Handle EQ launch events

  Scenario: EQ launched events are logged and the case flag is updated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    And a print action rule has been created
    Then UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    When an EQ_LAUNCH event is received
    And the events logged against the case are [NEW_CASE,PRINT_FILE,EQ_LAUNCH]
