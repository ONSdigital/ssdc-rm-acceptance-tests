Feature: SRM supports simple, email driven surveys

  @regression
  @reset_notify_stub
  Scenario: A simple email sample driven survey can be run in SRM
    Given the sample file "email_driven.csv" with validation rules "email_driven_rules.json" is loaded successfully
    And an email template has been created with template "sensitive_emailaddress__uac"
    When an email action rule has been created
    Then 5 UAC_UPDATE messages are emitted with active set to true
    And notify api was called with the correct emails from sample field "emailAddress" and notify template
