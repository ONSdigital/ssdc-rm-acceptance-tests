Feature: Un-submitted eQ partials can be flushed automatically by action rule

  Scenario: An eQ flush action rule generates the correct PubSub cloud task messages
    Given sample file "1_ROW_EMAIL.csv" with sensitive columns ["emailAddress"] is loaded successfully
    And an email template has been created with template ["__uac__"]
    And an email action rule has been created
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is false
    And an EQ_LAUNCH event is received
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    When an EQ flush action rule has been created
    Then an EQ_FLUSH cloud task queue message is sent for the correct QID