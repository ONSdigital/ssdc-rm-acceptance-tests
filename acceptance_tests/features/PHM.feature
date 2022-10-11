Feature: SRM supports PHM shape surveys

  @regression
  Scenario: A (prototype) PHM shape sample can be loaded
    Given the sample file "PHM_prototype_dummy_sample.csv" with validation rules "PHM_prototype_validation_rules.json" is loaded successfully

  @regression
  Scenario: A (prototype) PHM "wave" pattern can be scheduled with action rules
    # Sends an pre-notification of the test wave, with an opt out survey uac,
    # then a test survey UAC to those cases with a wave 1 opt out UAC which hasn't receipted,
    # then a reminder letter to those cases with a wave 1 test survey UAC which hasn't receipted
    Given the sample file "PHM_prototype_dummy_sample.csv" with validation rules "PHM_prototype_validation_rules.json" is loaded successfully
    And an export file template has been created with template ["FULL_NAME","ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]
    And an export file action rule has been created with UAC metadata "{"wave":"1","opt_out":true}" and classifiers "sample ->> 'NEXT_WAVE' = '1' AND sample_sensitive ->> 'EMAIL' = ''"
    And 2 UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And an export file template has been created with template ["FULL_NAME","ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]
    Then an export file action rule has been created with UAC metadata "{"wave":"1","test_survey":true}" and classifiers "sample_sensitive ->> 'EMAIL' = '' AND EXISTS (SELECT 1 FROM casev3.uac_qid_link WHERE caze_id = casev3.cases.id AND metadata ->> 'wave' = '1' AND (metadata ->> 'opt_out')::boolean AND NOT receipt_received)"
    And 2 UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows
    And an export file template has been created with template ["FULL_NAME","ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE","__uac__"]
    Then an export file action rule has been created with classifiers "sample_sensitive ->> 'EMAIL' = '' AND EXISTS (SELECT 1 FROM casev3.uac_qid_link WHERE caze_id = casev3.cases.id AND metadata ->> 'wave' = '1' AND (metadata ->> 'test_survey')::boolean AND NOT receipt_received)"
    And 2 UAC_UPDATE messages are emitted with active set to true
    And an export file is created with correct rows