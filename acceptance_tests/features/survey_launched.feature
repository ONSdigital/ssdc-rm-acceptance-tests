Feature: Handle survey launch events

  Scenario: Survey launched events are logged and the case flag is updated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    And a print action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a SURVEY_LAUNCH event is received with email address "SurveyLaunched"
    Then a CASE_UPDATE message is emitted where "surveyLaunched" is "True"
    And the events logged against the case are [NEW_CASE,PRINT_FILE,SURVEY_LAUNCH]
