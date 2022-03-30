Feature: SRM supports simple, email driven surveys

  Scenario: A simple email sample driven survey can be run in SRM
    Given the sample file "email_driven.csv" with validation rules "email_driven_rules.json" is loaded successfully
    And an email template has been created with template ["__sensitive__.emailAddress","__uac__"]
    When an email action rule has been created
    Then 5 UAC_UPDATE messages are emitted with active set to true
