Feature: Sample files of all accepted shapes can be loaded

  Scenario: A BOM sample file is loaded
    Given BOM sample file "LMS_Test_Sample_RM_BOM.csv" is loaded successfully
    And an export file template has been created with template ["ADDRESS_LINE1","ADDRESS_LINE2","POSTCODE"]
    When an export file action rule has been created
    And an export file is created with correct rows