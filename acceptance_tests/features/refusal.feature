Feature: A case can be refused with an event

  @regression
  Scenario: A case is loaded and can be refused
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When a refusal event is received and erase data is "false"
    Then a CASE_UPDATE message is emitted where "refusalReceived" is "EXTRAORDINARY_REFUSAL"
    And the events logged against the case are ["NEW_CASE","REFUSAL"]


  Scenario: A case is loaded and can be refused and data requested to be erased
    Given sample file "sample_1_limited_address_fields.csv" is loaded successfully
    When a refusal event is received and erase data is "true"
    Then a CASE_UPDATE message is emitted where {"refusalReceived": "EXTRAORDINARY_REFUSAL", "sampleSensitive": null,"invalid":true} are the updated values
    And the events logged against the case are ["NEW_CASE","REFUSAL","ERASE_DATA"]