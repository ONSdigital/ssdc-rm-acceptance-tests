Feature: Handle respondent authenticated events

  Scenario: A case is loaded and a respondent can authenticate against it
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "["__uac__"]"
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a UAC_AUTHENTICATION event is received
    Then the events logged against the case are ["NEW_CASE","EXPORT_FILE","UAC_AUTHENTICATION"]
