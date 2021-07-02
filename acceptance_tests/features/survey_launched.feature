Feature: Handle survey launch events

  Scenario: Survey launched events are logged and the case flag is updated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print wave of contact has been created with template "["__uac__"]" and classifiers "1=1"
    And UAC_UPDATED messages are emitted with active set to true
    When a SURVEY_LAUNCHED event is received
    Then a CASE_UPDATED message is emitted where "surveyLaunched" is "True"
    And the events logged against the case are [SAMPLE_LOADED,PRINTED_PACK_CODE,SURVEY_LAUNCHED]
