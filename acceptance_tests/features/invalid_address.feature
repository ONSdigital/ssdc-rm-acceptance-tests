Feature: An address can be invalidated with an event

  Scenario: A case is loaded and can be set to address invalid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print action rule has been created with template "["__uac__"]" and classifiers "1=1"
    And UAC_UPDATED messages are emitted with active set to true
    When an ADDRESS_NOT_VALID event is received
    Then a CASE_UPDATED message is emitted where "invalidAddress" is "True"
    And the events logged against the case are [SAMPLE_LOADED,PRINTED_PACK_CODE,ADDRESS_NOT_VALID]
