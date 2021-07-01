
Feature: launch a survey

  Scenario: A case is loaded and can have a survey launched
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created with template "["__uac__"]" and classifiers "1=1"
    And uac_updated msgs are emitted with active set to true
    When a survey launched msg is put on the queue
    Then a case_updated msg is emitted where "surveyLaunched" is "True"
    And the events logged for the survey launched case are [SAMPLE_LOADED,PRINTED_PACK_CODE,SURVEY_LAUNCHED]