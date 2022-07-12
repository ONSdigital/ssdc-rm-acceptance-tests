@web
Feature: Test RH-UI

  Scenario: Bad UAC entry display meesage
    Given the UAC entry page is displayed
    When the user enters UAC "PK39HN572FZFVHLQ"
    Then page displays string "Enter a valid access code"
