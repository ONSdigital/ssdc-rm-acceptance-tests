Feature: SSDC supports SIS surveys

  @regression
  Scenario: An SIS shape sample can be loaded
    Given the sample file "SIS2_random_20.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully