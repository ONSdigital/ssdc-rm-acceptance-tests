Feature: Check exception manager is called for every topic and handles them as expected

  Scenario: Bad Json Msg sent to every topic, msg arrives in exception manager
    When a bad json msg is sent to every topic consumed by RM
    Then each bad msg is seen by exception manager with the message containing "com.fasterxml.jackson.core.JsonParseException"
    And each bad msg can be successfully quarantined

  Scenario: Deactivate unknown UAC turns up in exception manager
    When a bad deactivate uac message is put on the topic
    Then a bad message appears in exception manager with exception message containing "Questionnaire Id '123456789' not found!"
    And each bad msg can be successfully quarantined

  Scenario: Bad invalid case message turns up in exception manager
    When a bad invalid case message is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case ID '7abb3c15-e850-4a9f-a0c2-6749687915a8' not present"
    And each bad msg can be successfully quarantined

  Scenario: Bad receipt message turns up in exception manager
    When a bad receipt message is put on the topic
    Then a bad message appears in exception manager with exception message containing "Questionnaire Id '987654321' not found!"
    And each bad msg can be successfully quarantined

  Scenario: Bad refusal message turns up in exception manager
    When a bad refusal event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case ID '1c1e495d-8f49-4d4c-8318-6174454eb605' not present"
    And each bad msg can be successfully quarantined

  Scenario: Bad respondent authenticated message turns up in exception manager
    When a bad respondent authenticated event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Questionnaire Id '666' not found!"
    And each bad msg can be successfully quarantined

  Scenario: Bad update sample message turns up in exception manager
    When a bad update sample event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case ID '386a50b8-6ba0-40f6-bd3c-34333d58be90' not present"
    And each bad msg can be successfully quarantined

  Scenario: Bad update sample sensitive message turns up in exception manager
    When a bad update sample sensitive event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case ID '386a50b8-6ba0-40f6-bd3c-34333d58be90' not present"
    And each bad msg can be successfully quarantined

  Scenario: Bad EQ launched message turns up in exception manager
    When a bad EQ launched event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Questionnaire Id '555555' not found!"
    And each bad msg can be successfully quarantined

  Scenario: Bad new case message turns up in exception manager
    Given the sample file "sis_survey_link.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When an invalid newCase event is put on the topic
    Then a bad message appears in exception manager with exception message containing "New case event failed validation on column "schoolId""
    And each bad msg can be successfully quarantined

  Scenario: Bad new case message turns up in exception manager
    Given the sample file "sis_survey_link.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When an invalid newCase event with extra sensitive data is put on the topic
    Then a bad message appears in exception manager with exception message containing "Attempt to send sensitive data to RM which was not part of defined sample"
    And each bad msg can be successfully quarantined