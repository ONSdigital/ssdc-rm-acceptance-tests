Feature: printfiles created with correct data

  Scenario Outline: A case is loaded, wave of contact triggered and printfile created with differing templates
    Given sample file "<sample file>" is loaded successfully
    When a wave of contact has been created with template "<template>" and classifiers "1=1"
    Then uac_updated msgs are emitted with active set to true
    And a print file is created with correct rows

    Examples:
      | sample file                      | template                                               |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"] |
      | business_sample_6_lines.csv      | ["BUSINESS_NAME","TOWN_NAME","__uac__","INDUSTRY"]     |


  Scenario Outline: A case is loaded wave of contact triggered and printfile created with differing classifiers
    Given sample file "<sample file>" is loaded successfully
    When a wave of contact has been created with template "["__uac__"]" and classifiers "<classifiers>"
    Then a print file is created expected row count of <expected row count>

    Examples:
      | sample file                 | classifiers                                                                             | expected row count |
      | business_sample_6_lines.csv | sample ->> 'ORG_SIZE' = 'HUGE'                                                          | 2                  |
      | business_sample_6_lines.csv | sample ->> 'INDUSTRY' IN ('MARKETING','FRUIT') AND (sample ->>'EMPLOYEES')::INT > 10000 | 3                  |
