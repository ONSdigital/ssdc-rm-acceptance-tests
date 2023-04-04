Feature: Export files can be created and sent with correct data

  Scenario Outline: A case is loaded, action rule triggered and export file created with differing templates with UACs
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template <template>
    When an export file action rule has been created
    Then UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And the events logged against the cases are ["NEW_CASE","EXPORT_FILE"]

    Examples:
      | sample file                      | template                                               |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"] |

    @regression
    Examples:
      | sample file                 | template                                                     |
      | business_sample_6_lines.csv | ["BUSINESS_NAME","TOWN_NAME","__uac__","__qid__","INDUSTRY"] |

  Scenario: Export file containing sensitive case fields
    Given the sample file "CRIS_dummy_1_row.csv" with validation rules "CRIS_validation_rules_v1.json" is loaded successfully
    And an export file template has been created with template ["__sensitive__.MIDDLE_NAME","__sensitive__.LAST_NAME"]
    When an export file action rule has been created
    And an export file is created with correct rows
    And the events logged against the cases are ["NEW_CASE","EXPORT_FILE"]

  Scenario Outline: A case is loaded, action rule triggered and export file created with differing templates no UACs
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template <template>
    When an export file action rule has been created
    And an export file is created with correct rows
    And the events logged against the cases are ["NEW_CASE","EXPORT_FILE"]

    Examples:
      | sample file                      | template                                     |
      | social_sample_3_lines_fields.csv | ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE"] |

    @regression
    Examples:
      | sample file                 | template                                 |
      | business_sample_6_lines.csv | ["BUSINESS_NAME","TOWN_NAME","INDUSTRY"] |

  Scenario Outline: A case is loaded action rule triggered and export file created with differing classifiers
    Given sample file "<sample file>" is loaded successfully
    And an export file template has been created with template ["__uac__"]
    When an export file action rule has been created with classifiers "<classifiers>"
    Then <expected row count> UAC_UPDATE messages are emitted with active set to true
    Then an export file is created with correct rows
    And the events logged against the cases are ["NEW_CASE","EXPORT_FILE"]

    Examples:
      | sample file                 | classifiers                    | expected row count |
      | business_sample_6_lines.csv | sample ->> 'ORG_SIZE' = 'HUGE' | 2                  |

    @regression
    Examples:
      | sample file                 | classifiers                                                                             | expected row count |
      | business_sample_6_lines.csv | sample ->> 'INDUSTRY' IN ('MARKETING','FRUIT') AND (sample ->>'EMPLOYEES')::INT > 10000 | 3                  |

  @cloud_only
  Scenario: Notification messages are sent to a pubsub subscription to notify NIFI of export files in the configured supplier location
    Given sample file "CRIS_dummy_1_row.csv" is loaded successfully
    And an export file template has been created for the internal reprographics supplier with template ["FIRST_NAME", "POSTCODE"]
    And an export file action rule has been created
    When an export file is created with correct rows
    Then a notification PubSub message is sent to NIFI with the correct export file details
