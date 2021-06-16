Feature: printfiles created with correct data

  Scenario Outline: A case is loaded wave of contact triggered and printfile created
    Given sample file "<sample file>" is loaded successfully
    When a wave of contact has been created with template "<template>"
    Then a uac_updated msg is emitted with active set to true
    And a print file is created with correct rows

    Examples: Reminder contact letter: <pack code>
      | sample file                        | template                                               |
      | social_sample_3_lines_fields.csv   | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"] |
      | business_sample_4_lines_fields.csv | ["BUSINESS_NAME","TOWN_NAME","__uac__","INDUSTRY"]    |