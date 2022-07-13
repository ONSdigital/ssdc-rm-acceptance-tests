@web
Feature: Test UI

  Scenario: Works with RH-UI, Bad UAC entry display meesage
    Given the UAC entry page is displayed
    When the user enters UAC "PK39HN572FZFVHLQ"
    Then link text displays string "Enter a valid access code"

  Scenario: Works with a good UAC
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template ["__uac__"]
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    When the UAC entry page is displayed
    And the user enters a valid UAC
    Then they are redirected to EQ

  Scenario: A receipted UAC redirects to informative page
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template ["__uac__"]
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    When a receipt message is published to the pubsub receipting topic
    Then UAC_UPDATE message is emitted with active set to false and "receiptReceived" is true
    And the events logged against the case are ["NEW_CASE","EXPORT_FILE","RECEIPT"]
    When the UAC entry page is displayed
    And the user enters a receipted UAC
    Then they are redirected to the receipted page

  Scenario: A deactived UAC redirects to informative page
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    And an export file template has been created with template ["__uac__"]
    And an export file action rule has been created
    And UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    When a deactivate uac action rule has been created
    Then UAC_UPDATE messages are emitted with active set to false
    When the UAC entry page is displayed
    And the user enters an inactive UAC
    Then they are redirected to the inactive uac page

  Scenario: No access code entered
    Given the UAC entry page is displayed
    When the user clicks Access Survey without entering a UAC
    Then link text displays string "Enter an access code"

#    here as a proof of concept
  Scenario: Works with Support Tool
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    Then I navigate to support tool home
    Then I use the survey Id to click on the created survey
    Then page displays string "Survey: test survey"
