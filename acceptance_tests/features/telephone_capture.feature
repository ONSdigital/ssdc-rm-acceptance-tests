
Feature: Telephone capture

  Scenario: A case can be completed using telephone capture
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When there is a request for telephone capture of a case
    Then a UAC and QID with questionnaire type "01" type are generated and returned
    And the events logged for the case requesting telephone capture are [SAMPLE_LOADED,TELEPHONE_CAPTURE_REQUESTED]