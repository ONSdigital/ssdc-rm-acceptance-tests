Feature: Launch a survey with a claims token from Respondent Home UI using a UAC

  @reset_notify_stub
  Scenario: Post a UAC to the launch endpoint and get redirected to a launch URL with a claims token
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for sms template "uac__qid"
    And a request has been made for a replacement UAC by SMS from phone number "07123456789"
    And UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And we retrieve the UAC and QID from the SMS fulfilment to use for launching in RH
    When the respondent home UI launch endpoint is called with the UAC
    Then it redirects to a launch URL with a launch claims token
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
    And the events logged against the case are ["NEW_CASE","SMS_FULFILMENT","EQ_LAUNCH"]