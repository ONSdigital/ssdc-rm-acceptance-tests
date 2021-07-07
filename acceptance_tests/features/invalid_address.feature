Feature: An address can be invalidated with an event

  Scenario: A case is loaded and can be set to address invalid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When an ADDRESS_NOT_VALID event is received
    Then a CASE_UPDATED message is emitted where "invalidAddress" is "True"
    And the events logged against the case are [SAMPLE_LOADED,ADDRESS_NOT_VALID]
