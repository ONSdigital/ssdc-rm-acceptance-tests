Feature: A case can be receipted with an event

  Scenario: A case is loaded and can be receipted
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "uac"
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a receipt message is published to the pubsub receipting topic
    Then UAC_UPDATE message is emitted with active set to false and "receiptReceived" is true
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","RECEIPT"]
