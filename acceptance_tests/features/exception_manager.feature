
Feature:

    Scenario: Bad Msg sent to topic, msg arrives in exception manager
    When a bad json msg is sent to every topic consumed by RM
    Then each bad msg is seen by exception manager
