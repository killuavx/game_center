Feature: update client
  As a Player
  I want to receive client version update message from game center
  So that I can pay attention to new function of the client at first time

  Scenario: client has nothing can selfupdate
    Given nothing can selfupdate
    When I visit selfupdate
    Then I should receive 204 No Content
