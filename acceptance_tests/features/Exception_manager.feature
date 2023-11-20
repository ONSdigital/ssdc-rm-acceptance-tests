Feature: Check exception manager is called for every topic and handles them as expected

  # Scenarion labelled 1 as we want this one to run at the beginning of the tests as a way of warming up pubsub
  Scenario: 1: A Bad Json Msg sent to every topic, msg arrives in exception manager
    When a bad json msg is sent to every topic consumed by RM
    Then each bad msg is seen by exception manager with the message containing "com.fasterxml.jackson.core.JsonParseException"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Deactivate unknown UAC turns up in exception manager
    When a bad deactivate uac message is put on the topic
    Then a bad message appears in exception manager with exception message containing "qid '123456789' not found!"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad invalid case message turns up in exception manager
    When a bad invalid case message is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case with ID '7abb3c15-e850-4a9f-a0c2-6749687915a8' not found"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad receipt message turns up in exception manager
    When a bad receipt message is put on the topic
    Then a bad message appears in exception manager with exception message containing "qid '987654321' not found!"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad refusal message turns up in exception manager
    When a bad refusal event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case with ID '1c1e495d-8f49-4d4c-8318-6174454eb605' not found"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad update sample message turns up in exception manager
    When a bad update sample event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case with ID '386a50b8-6ba0-40f6-bd3c-34333d58be90' not found"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad update sample sensitive message turns up in exception manager
    When a bad update sample sensitive event is put on the topic
    Then a bad message appears in exception manager with exception message containing "Case with ID '386a50b8-6ba0-40f6-bd3c-34333d58be90' not found"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad EQ launched message turns up in exception manager
    When a bad EQ launched event is put on the topic
    Then a bad message appears in exception manager with exception message containing "qid '555555' not found!"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad new case message turns up in exception manager
    Given the sample file "sis_survey_link.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When an invalid newCase event is put on the topic
    Then a bad message appears in exception manager with exception message containing "NEW_CASE event: Column 'schoolId' Failed validation for Rule 'LengthRule' validation error: Exceeded max length of 11"
    And each bad msg can be successfully quarantined

  @regression
  Scenario: Bad new case message turns up in exception manager
    Given the sample file "sis_survey_link.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When an invalid newCase event with extra sensitive data is put on the topic
    Then a bad message appears in exception manager with exception message containing "Attempt to send sensitive data to RM which was not part of defined sample"
    And each bad msg can be successfully quarantined