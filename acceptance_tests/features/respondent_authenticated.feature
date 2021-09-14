Feature: Handle respondent authenticated events

  Scenario: A case is loaded and a respondent can authenticate against it
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And a print template has been created with template "["__uac__"]"
    And a print action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a UAC_AUTHENTICATION event is received with email address "RespondentAuthenticated"
    Then the events logged against the case are [NEW_CASE,PRINT_FILE,UAC_AUTHENTICATION]
