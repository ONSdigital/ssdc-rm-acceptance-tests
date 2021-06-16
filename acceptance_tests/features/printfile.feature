
Feature: printfiles created with correct data

  Scenario: A case is loaded wave of contact triggered and printfile created
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    And a wave of contact has been created with template "["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]"
    And a uac_updated msg is emitted with active set to true
    When a print file is created with correct rows
