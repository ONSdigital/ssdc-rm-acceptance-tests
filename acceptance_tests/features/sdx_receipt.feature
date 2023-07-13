Feature: A case can be receipted with an event from sdx

  Scenario: A case is loaded and can be receipted
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And fulfilments are authorised for email template "uac__qid"
    When a request has been made for a replacement UAC by email from email address "foo@bar.baz"
    Then UAC_UPDATE messages are emitted with active set to true
    And the UAC_UPDATE message matches the email fulfilment UAC
    When a receipt message is published to the sdx pubsub receipting topic
    Then UAC_UPDATE messages are emitted for the correct cases with active set to false and "receiptReceived" is true
    And the events logged against the case are ["NEW_CASE","EMAIL_FULFILMENT","RECEIPT"]
