Feature: scheduled tasks
#
  Scenario: Upload a Schedule Template, scheduled tasks create

    When create survey with template "CIS_simple_schedule.json" and load sample file "sample_1_limited_address_fields.csv"
    Then the expected schedule is created against the new case in the database
    And that the expected scheduledTasks are created in the database

#    Given CIS_simple_schedule.json     I create a survey with schedule template "ScheduledTemplate.json"
#    When I upload a new Case for this survey
#    Then Expected ScheduledTask Exists
#    And Expected ScheduledTask Json exist against Case
#
#

