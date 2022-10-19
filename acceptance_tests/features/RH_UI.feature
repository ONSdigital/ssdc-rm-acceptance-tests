@UI
Feature: Testing the "enter a UAC" functionality of RH UI

  Scenario Outline: Entering a bad UAC and error section displayed X
    Given the UAC entry page is displayed for <language code>
    When the user enters UAC "PK39HN572FZFVHLQ"
    Then an error section is headed <error section header> and href "#uac_invalid" is <expected error text>
    And link text displays string <expected link test>

    Examples:
      | language code | expected error text                           | error section header                               | expected link test                            |
      | "en"          | "Enter a valid access code"                   | "There is a problem with this page"                | "Enter a valid access code"                   |
      | "cy"          | "PLACEHOLDER WELSH Rhowch god mynediad dilys" | "PLACEHOLDER WELSH Mae problem gyda'r dudalen hon" | "PLACEHOLDER WELSH Rhowch god mynediad dilys" |

  @reset_notify_stub
  Scenario Outline: Works with a good UAC
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an sms template has been created with template ["__uac__", "__qid__"]
    And fulfilments are authorised on sms template
    And a request has been made for a replacement UAC by SMS from phone number "07123456789"
    And UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And we retrieve the UAC and QID from the SMS fulfilment to use for launching in RH
    And check UAC is in firestore via eqLaunched endpoint for the correct <language code>
    When the UAC entry page is titled <expected text> and is displayed for <language code>
    And the user enters a valid UAC
    Then they are redirected to EQ with the correct token and language set to <language code>
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true

    Examples:
      | language code | expected text                                 |
      | "en"          | "Start study - ONS Surveys"                   |
      | "cy"          | "PLACEHOLDER WELSH Start study - ONS Surveys" |

  @reset_notify_stub
  Scenario: A receipted UAC redirects to informative page
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an sms template has been created with template ["__uac__", "__qid__"]
    And fulfilments are authorised on sms template
    And a request has been made for a replacement UAC by SMS from phone number "07123456789"
    And UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And we retrieve the UAC and QID from the SMS fulfilment to use for launching in RH
    And a receipt message is published to the pubsub receipting topic
    And UAC_UPDATE message is emitted with active set to false and "receiptReceived" is true
    And the events logged against the case are ["NEW_CASE","SMS_FULFILMENT","RECEIPT"]
    When the UAC entry page is displayed
    And the user enters a receipted UAC
    Then they are redirected to the receipted page

  @reset_notify_stub
  Scenario: A deactivated UAC redirects to informative page
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an sms template has been created with template ["__uac__", "__qid__"]
    And fulfilments are authorised on sms template
    And a request has been made for a replacement UAC by SMS from phone number "07123456789"
    And UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the SMS fulfilment UAC
    And we retrieve the UAC and QID from the SMS fulfilment to use for launching in RH
    And a deactivate uac message is put on the queue
    And UAC_UPDATE messages are emitted with active set to false
    When the UAC entry page is displayed
    And the user enters an inactive UAC
    Then they are redirected to the inactive uac page

  Scenario: No access code entered
    Given the UAC entry page is displayed
    When the user clicks Access Survey without entering a UAC
    Then an error section is displayed with href "#uac_empty" is displayed with "Enter an access code"