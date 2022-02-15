Feature: scheduled tasks
#
#  Scenario: Upload a Schedule Template, scheduled tasks create
#    When create survey with template "CIS_simple_schedule.json" and load sample file "sample_1_limited_address_fields.csv"
#    Then the expected schedule is created against the new case in the database
#    And that the expected scheduledTasks are created in the database

  Scenario: Upload a Schedule Template, scheduled tasks created and export file produced
    When create survey with template "CIS_simple_schedule.json" and load sample file "sample_1_limited_address_fields.csv"
    Then the expected schedule is created against the new case in the database
    And that the expected scheduledTasks are created in the database
    And for each schedule packcodes an export file template has been created with template "["ADDRESS_LINE1","POSTCODE"]"
    And fulfilments are authorised on the export file template for all the packcodes
    And check that a scheduledTask is processed and removed from the database
    When export file fulfilments are triggered to be exported
    And check that the schedule against the case is as expected
    And the correct export files are created for the schedule

#    Then UAC_UPDATE messages are emitted with active set to true
#    And an export file is created with correct rows
#    And the events logged against the case are [NEW_CASE,EXPORT_FILE,PRINT_FULFILMENT]

#    And the scheduledTasks look like this

#    Given CIS_simple_schedule.json     I create a survey with schedule template "ScheduledTemplate.json"
#    When I upload a new Case for this survey
#    Then Expected ScheduledTask Exists
#    And Expected ScheduledTask Json exist against Case
#
#

