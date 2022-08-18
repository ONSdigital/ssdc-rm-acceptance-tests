@UI
Feature: Test basic Support Tool Functionality

  Scenario: Create a Survey, Collection Exercise and Load a Sample
    Given the support tool landing page is displayed
    And The Create Survey Button is clicked on
    And a Survey called "CreateSurveyTest" plus unique suffix is created for sample file "social_sample_3_lines_fields.csv"
    When the survey is clicked on it should display the collex page
    And the create collection exercise button is clicked on and entered in details
    And the collex is clicked on and displays the details page
    And I click the upload sample file button with file "social_sample_3_lines_fields.csv"


#  Do all of the above in a single step too for other tests