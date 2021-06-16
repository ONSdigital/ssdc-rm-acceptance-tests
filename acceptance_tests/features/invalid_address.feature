
Feature: invalidating a case with invalid address msg

  Scenario: A case is loaded and can be set to address invalid
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created
    And a uac_updated msg is emitted with active set to true
    When a invalid address msg is put on the queue
    Then a case_updated msg is emitted where "invalidAddress" is "True"
