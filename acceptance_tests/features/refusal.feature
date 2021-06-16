
Feature: refusing a case

  Scenario: A case is loaded and can be refused
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created
    And a uac_updated msg is emitted with active set to true
    When a case refused msg is put on the queue
    Then a case_updated msg is emitted where "refusalReceived" is "EXTRAORDINARY_REFUSAL"