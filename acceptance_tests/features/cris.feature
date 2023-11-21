Feature: SRM supports CRIS shape surveys

  @regression
  Scenario: A CRIS shape sample can be loaded
    Given the sample file "CRIS_dummy_2_rows.csv" with validation rules "CRIS_validation_rules_v1.json" is loaded successfully