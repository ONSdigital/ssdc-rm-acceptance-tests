Feature: Loading a file in RM, results in data in RH

  @rh
  Scenario: Load a file in RM, poll RH
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully for survey type "social"
    When the rh-service api is polled for attribute "ADDRESS_LINE1" and value "Something View" the correct case is returned