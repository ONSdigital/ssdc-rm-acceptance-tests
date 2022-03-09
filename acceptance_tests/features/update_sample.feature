Feature: Sample data in the case can be updated

  Scenario: A case is loaded and data can be changed
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When an UPDATE_SAMPLE event is received updating the ADDRESS_LINE1 to Test Street
    Then the ADDRESS_LINE1 in the data on the case has been updated to Test Street
    And a CASE_UPDATED message is emitted for the case
    And the events logged against the case are ["NEW_CASE","UPDATE_SAMPLE"]
