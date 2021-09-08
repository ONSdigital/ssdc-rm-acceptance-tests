Feature: Print files can be created and sent with correct data

  Scenario Outline: A case is loaded, action rule triggered and print file created with differing templates with UACs
    Given sample file "<sample file>" is loaded successfully
    And a print template has been created with template "<template>"
    When a print action rule has been created
    Then UAC_UPDATE messages are emitted with active set to true
    And a print file is created with correct rows

    Examples:
      | sample file                      | template                                                     |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]       |
      | business_sample_6_lines.csv      | ["BUSINESS_NAME","TOWN_NAME","__uac__","__qid__","INDUSTRY"] |

  Scenario Outline: A case is loaded, action rule triggered and print file created with differing templates no UACs
    Given sample file "<sample file>" is loaded successfully
    And a print template has been created with template "<template>"
    When a print action rule has been created
    And a print file is created with correct rows

    Examples:
      | sample file                      | template                                     |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE"] |
      | business_sample_6_lines.csv      | ["BUSINESS_NAME","TOWN_NAME","INDUSTRY"]     |

  Scenario Outline: A case is loaded action rule triggered and print file created with differing classifiers
    Given sample file "<sample file>" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    When a print action rule has been created with classifiers "<classifiers>"
    Then <expected row count> UAC_UPDATE messages are emitted with active set to true
    Then a print file is created with correct rows

    Examples:
      | sample file                 | classifiers                                                                             | expected row count |
      | business_sample_6_lines.csv | sample ->> 'ORG_SIZE' = 'HUGE'                                                          | 2                  |
      | business_sample_6_lines.csv | sample ->> 'INDUSTRY' IN ('MARKETING','FRUIT') AND (sample ->>'EMPLOYEES')::INT > 10000 | 3                  |


  Scenario Outline: A BOM sample file is loaded
    Given BOM sample file "<sample file>" is loaded successfully
    And a print template has been created with template "<template>"
    When a print action rule has been created
    And a print file is created with correct rows

    Examples:
      | sample file                | template                                     |
      | LMS_Test_Sample_RM_BOM.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE"] |

