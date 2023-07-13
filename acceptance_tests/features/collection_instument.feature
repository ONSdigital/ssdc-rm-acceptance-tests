
Feature: choose collection instruments for cases

  @regression
  Scenario: A selection rule chooses the correct collection instrument based on case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully with complex case CI selection rules
    And an export file template has been created with template "uac"
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true

  Scenario: A selection rule chooses the correct collection instrument based on UAC metadata and case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully with complex UAC CI selection rules
    And fulfilments are authorised for sms template "uac__qid"
    When a request has been made for a replacement UAC by SMS from phone number "07123456789"
    Then UAC_UPDATE messages are emitted with active set to true
