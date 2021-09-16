Feature: Handle survey launch events

  Scenario: Survey launched events are logged and the case flag is updated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    And a print action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When an EQ_LAUNCH event is received with email address "EQLaunched"
    Then a CASE_UPDATE message is emitted where "eqLaunched" is "True"
    And the events logged against the case are [NEW_CASE,PRINT_FILE,EQ_LAUNCH]
