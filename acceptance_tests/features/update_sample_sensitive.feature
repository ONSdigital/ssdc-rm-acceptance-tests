Feature: Sensitive sample data in the case can be updated

  Scenario: A case is loaded and sensitive data can be changed
    Given sample file "sensitive_data_sample.csv" with sensitive columns ["PHONE_NUMBER"] is loaded successfully
    When an UPDATE_SAMPLE_SENSITIVE event is received updating the PHONE_NUMBER to 07898787878
    Then the PHONE_NUMBER in the sensitive data on the case has been updated to 07898787878
    And a CASE_UPDATED message is emitted for the case with correct sensitive data
    And the events logged against the case are ["NEW_CASE","UPDATE_SAMPLE_SENSITIVE"]
