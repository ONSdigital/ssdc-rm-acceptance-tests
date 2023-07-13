Feature: Handle EQ launch events

  Scenario: EQ launched events are logged and the case flag is updated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "uac"
    And an export file action rule has been created
    Then UAC_UPDATE message is emitted with active set to true and "eqLaunched" is false
    When an EQ_LAUNCH event is received
    Then UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","EQ_LAUNCH"]
