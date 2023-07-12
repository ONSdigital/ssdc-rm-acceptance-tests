Feature: Sample files of all accepted shapes can be loaded

  @regression
  Scenario: A BOM sample file is loaded
    Given BOM sample file "LMS_Test_Sample_RM_BOM.csv" is loaded successfully
    And an export file template has been created with template "address_line1__address_line2__postcode"
    When an export file action rule has been created
    And an export file is created with correct rows