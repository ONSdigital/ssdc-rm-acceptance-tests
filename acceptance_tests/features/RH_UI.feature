@UI
Feature: Testing the "enter a UAC" functionality of RH UI

  Scenario Outline: Entering a bad UAC and error section displayed X
    Given the UAC entry page is displayed for "<language code>"
    When the user enters UAC "PK39HN572FZFVHLQ"
    Then an error section is headed "<error section header>" and href "#uac_invalid" is "<expected error text>"
    And link text displays string "<expected link test>"

    Examples:
      | language code | expected error text                                          | error section header              | expected link test                                           |
      | en            | Access code not recognised. Enter the code again.            | There is a problem with this page | Access code not recognised. Enter the code again.            |
      | cy            | Nid yw'r cod mynediad yn cael ei gydnabod. Rhowch y cod eto. | Mae problem gyda'r dudalen hon    | Nid yw'r cod mynediad yn cael ei gydnabod. Rhowch y cod eto. |

  @reset_notify_stub
  Scenario Outline: Works with a good UAC
    Given sample file "CRIS_dummy_1_row.csv" is loaded successfully
    And and we request a UAC by SMS and the UAC is ready and RH page has "<expected text>" for "<language code>"
    And the user enters a valid UAC
    Then they are redirected to EQ with the correct token and language set to "<language code>"
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true

    Examples:
      | language code | expected text                       |
      | en            | Start study - ONS Surveys           |
      | cy            | Dechrau'r astudiaeth - Arolygon SYG |

  @reset_notify_stub
  Scenario: A receipted UAC redirects to informative page
    Given sample file "CRIS_dummy_1_row.csv" is loaded successfully
    And and we request a UAC by SMS and the UAC is ready and RH page has "Start study - ONS Surveys" for "en"
    And a receipt message is published to the pubsub receipting topic
    And UAC_UPDATE message is emitted with active set to false and "receiptReceived" is true
    And the events logged against the case are ["NEW_CASE", "EQ_LAUNCH", "SMS_FULFILMENT","RECEIPT"]
    And the user enters a receipted UAC
    Then they are redirected to the receipted page

  @reset_notify_stub
  Scenario: A deactivated UAC redirects to informative page
    Given sample file "CRIS_dummy_1_row.csv" is loaded successfully
    And and we request a UAC by SMS and the UAC is ready and RH page has "Start study - ONS Surveys" for "en"
    And a deactivate uac message is put on the queue
    And UAC_UPDATE messages are emitted with active set to false
    And the user enters an inactive UAC
    Then they are redirected to the inactive uac page

  Scenario: No access code entered
    Given the UAC entry page is displayed
    When the user clicks Access Survey without entering a UAC
    Then an error section is headed "There is a problem with this page" and href "#uac_empty" is "Enter an access code"

  @reset_notify_stub
  Scenario: Launching with survey metadata
    Given sample file "CRIS_dummy_1_row.csv" is loaded with rules "CRIS_validation_rules_v1.json" and eq launch settings set to "launchData.json"
    And and we request a UAC by SMS and the UAC is ready and RH page has "Start study - ONS Surveys" for "en"
    And the user enters a valid UAC
    Then they are redirected to EQ with the language "en" and the EQ launch settings file "launchData.json"
    And UAC_UPDATE message is emitted with active set to true and "eqLaunched" is true
