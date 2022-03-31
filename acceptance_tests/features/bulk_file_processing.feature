Feature: bulk file processed

  Scenario: After a sample is loaded the cases can be refused on bulk
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    When a bulk refusal file is created for every case created and uploaded
    Then a CASE_UPDATE message is emitted for each bulk updated case with expected refusal type

  @regression
  Scenario: After a sample is loaded the cases can be set as invalid
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    When a bulk invalid file is created for every case created and uploaded
    Then a CASE_UPDATE message is emitted for each bulk updated invalid case with correct reason

  @regression
  Scenario: After a sample is loaded the sample data can be updated
    Given the sample file "SIS2_random_20.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When a bulk sample update file is created for every case created and uploaded
    Then a CASE_UPDATE message is emitted for each bulk updated sample row

  @regression
  Scenario: After a sample is loaded the sensitive data can be updated
    Given the sample file "SIS2_random_20.csv" with validation rules "SIS2_validation_rules.json" is loaded successfully
    When a bulk sensitive update file is created for every case created and uploaded
    Then in the database the sensitive data has been updated as expected and is emitted redacted
