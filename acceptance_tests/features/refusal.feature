Feature: A case can be refused with an event

  Scenario: A case is loaded and can be refused
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When a REFUSAL event is received
    Then a CASE_UPDATE message is emitted where "refusalReceived" is "EXTRAORDINARY_REFUSAL"
    And the events logged against the case are [NEW_CASE,REFUSAL]
