
Feature: test receipting


  Scenario: A case is loaded and can be receipted
    Given sample file is loaded successfully
    And a wave of contact has been created
    And a uac_updated msg is emitted with active set to true for the receipted qid
    When the case has been receipted
    Then a uac_updated msg is emitted with active set to false
    And a case_updated msg is emitted where "receiptReceived" is "True"