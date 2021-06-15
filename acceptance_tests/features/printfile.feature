
Feature: printfiles created with correct data

  Scenario: A case is loaded wave of contact triggered and printfile created
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a wave of contact has been created
    And a uac_updated msg is emitted with active set to true
    When a print file is created
