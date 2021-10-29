Feature: bulk refusal file processed

  Scenario: After a sample is loaded the cases can be refused on bulk
    Given sample file "social_sample_3_lines_fields.csv" is loaded successfully
    When a bulk refusal file of type "EXTRAORDINARY_REFUSAL" is created for every case created and uploaded
    Then a CASE_UPDATE message is emitted for each bulk updated case with expected refusal type



