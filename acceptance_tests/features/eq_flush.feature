Feature: Un-submitted eQ partials can be flushed automatically by action rule

  @reset_notify_stub
  Scenario: An eQ flush action rule generates the correct PubSub cloud task messages
    Given sample file "1_ROW_EMAIL.csv" with sensitive columns ["emailAddress"] is loaded successfully
    And an email template has been created with template "uac"
    And an email action rule has been created
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is false
    And an EQ_LAUNCH event is received
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    When an EQ flush action rule has been created
    Then an EQ_FLUSH cloud task queue message is sent for the correct QID

  @cloud_only
  @reset_eq_stub
  @reset_notify_stub
  Scenario: An eQ flush action rule triggers the calls to the eQ flush endpoint
    Given sample file "1_ROW_EMAIL.csv" with sensitive columns ["emailAddress"] is loaded successfully
    And an email template has been created with template "uac__qid"
    And an email action rule has been created
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is false
    And we retrieve the UAC and QID from the email log to use for launching in RH
    And the respondent home UI launch endpoint is called with the UAC
    And it redirects to a launch URL with a launch claims token
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    When an EQ flush action rule has been created
    Then an EQ_FLUSH cloud task queue message is sent for the correct QID
    And the EQ flush endpoint is called with the token for flushing the correct QIDs partial
    And the EQ flush claims response ID matches the EQ launch claims response ID
