Feature: Sample data in the case is sensitive and must be redacted

  Scenario: A case is loaded and sensitive data can be changed
    Given sample file "sensitive_data_sample.csv" with sensitive column PHONE_NUMBER is loaded successfully
    When an UPDATE_SAMPLE_SENSITIVE event is received updating the PHONE_NUMBER to 07898787878 with email "SensitiveData"
    Then the PHONE_NUMBER in the sensitive data on the case has been updated to 07898787878
    And the events logged against the case are [NEW_CASE,UPDATE_SAMPLE_SENSITIVE]
