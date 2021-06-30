
Feature: Respondent authenticating


  Scenario: A case is loaded and a respondent can authenticate against it
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created with template "["__uac__"]" and classifiers "1=1"
    And uac_updated msgs are emitted with active set to true
    When a respondent authenticated msg is put on the queue
    Then the events logged for the case the respondent has authenticated against are [SAMPLE_LOADED,RESPONDENT_AUTHENTICATED]