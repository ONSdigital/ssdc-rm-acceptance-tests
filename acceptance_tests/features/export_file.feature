Feature: Export files can be created and sent with correct data

  Scenario Outline: A case is loaded, action rule triggered and export file created with differing templates with UACs
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template "<template>"
    When an export file action rule has been created
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows

    Examples:
      | sample file                      | template                                                     |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]       |
      | business_sample_6_lines.csv      | ["BUSINESS_NAME","TOWN_NAME","__uac__","__qid__","INDUSTRY"] |

  Scenario Outline: A case is loaded, action rule triggered and export file created with differing templates no UACs
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template "<template>"
    When an export file action rule has been created
    And an export file is created with correct rows

    Examples:
      | sample file                      | template                                     |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE"] |
      | business_sample_6_lines.csv      | ["BUSINESS_NAME","TOWN_NAME","INDUSTRY"]     |

  Scenario Outline: A case is loaded action rule triggered and export file created with differing classifiers
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template "["__uac__"]"
    When an export file action rule has been created with classifiers "<classifiers>"
    Then <expected row count> UAC_UPDATE messages are emitted with active set to true
    Then an export file is created with correct rows

    Examples:
      | sample file                 | classifiers                                                                             | expected row count |
      | business_sample_6_lines.csv | sample ->> 'ORG_SIZE' = 'HUGE'                                                          | 2                  |
      | business_sample_6_lines.csv | sample ->> 'INDUSTRY' IN ('MARKETING','FRUIT') AND (sample ->>'EMPLOYEES')::INT > 10000 | 3                  |
