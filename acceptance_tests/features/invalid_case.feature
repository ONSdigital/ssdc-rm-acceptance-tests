Feature: A case can be invalidated with an event

  Scenario: A case is loaded and can be set to invalid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When an INVALID_CASE event is received
    Then a CASE_UPDATE message is emitted where "invalid" is "True"
    And the events logged against the case are ["NEW_CASE","INVALID_CASE"]
