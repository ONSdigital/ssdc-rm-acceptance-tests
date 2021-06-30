
Feature: receipting a case

  Scenario: A case is loaded and can be receipted
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created with template "["__uac__"]" and classifiers "1=1"
    And uac_updated msgs are emitted with active set to true
    When the receipt msg is put on the GCP pubsub
    Then a uac_updated msg is emitted with active set to false
    And a case_updated msg is emitted where "receiptReceived" is "True"