Feature: A new case is submitted

 Scenario: A new case is submitted
   Given sample file "sis_survey_link.csv" with sensitive columns [PHONE_NUMBER,CHILD_NAME] is loaded successfully
   When a newCase event is built and submitted
   Then a CASE_UPDATED message is emitted for the new case
   And the event logged against the case is [NEW_CASE]
