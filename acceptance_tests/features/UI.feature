@web
Feature: Test UI

  Scenario: Works with RH-UI, Bad UAC entry display meesage
    Given the UAC entry page is displayed
    When the user enters UAC "PK39HN572FZFVHLQ"
    Then link text displays string "Enter a valid access code"

@skip
  Scenario: Works with Support Tool
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    Then I navigate to support tool home
    Then I use the survey Id to click on the created survey
    Then page displays string "Survey: test survey"
