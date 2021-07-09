Feature: Sample data in the case is sensitive and must be redacted

  Scenario: A case is loaded and sensitive data can be changed
    Given sample file "sensitive_data_sample.csv" with sensitive column PHONE_NUMBER is loaded successfully
    When an UPDATE_SAMPLE_SENSITIVE event is received
    Then the sensitive data on the case is changed
    And the events logged against the case are [SAMPLE_LOADED,UPDATE_SAMPLE_SENSITIVE]
