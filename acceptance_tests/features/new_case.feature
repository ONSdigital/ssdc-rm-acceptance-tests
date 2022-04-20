Feature: A new case is submitted

 Scenario: A new case is submitted
   Given sample file "sis_survey_link.csv" with sensitive columns ["firstName","lastName","childFirstName","childMiddleNames","childLastName","childDob","mobileNumber","emailAddress","consentGivenTest","consentGivenSurvey"] is loaded successfully
   When a newCase event is built and submitted
   Then a CASE_UPDATED message is emitted for the new case
   And the events logged against the case are ["NEW_CASE"]
