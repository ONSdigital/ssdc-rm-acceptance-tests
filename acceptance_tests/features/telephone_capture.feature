Feature: Telephone capture

  Scenario: A telephone capture UAC and QID can be requested from the case API
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When there is a request for telephone capture of a case
    Then a UAC and QID with questionnaire type "01" type are generated and returned
    And the events logged against the case are [SAMPLE_LOADED,TELEPHONE_CAPTURE_REQUESTED]
