Feature: deactivate UACs for a case

  @regression
  Scenario: A case is loaded, action rule is triggered and UAC is deactivated for that case
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "uac"
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a deactivate uac action rule has been created
    Then UAC_UPDATE messages are emitted with active set to false


  Scenario: A deactivate UAC event is received for a QID and the UAC is deactivated
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template "uac"
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    When a deactivate uac message is put on the queue
    Then UAC_UPDATE messages are emitted with active set to false