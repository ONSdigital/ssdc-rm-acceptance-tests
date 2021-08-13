Feature: A case can be receipted with an event

  Scenario: A case is loaded and can be receipted
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    And a print action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a receipt message is published to the pubsub receipting topic
    Then a UAC_UPDATE message is emitted with active set to false
    And a CASE_UPDATE message is emitted where "receiptReceived" is "True"
    And the events logged against the case are [NEW_CASE,PRINT_FILE,RECEIPT]
