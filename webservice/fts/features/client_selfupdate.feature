@wip
Feature: update client
  As a Player
  I want to receive client version update message from game center
  So that I can pay attention to new function of the client at first time

  Background:
    Given a browser or client

  Scenario: client has nothing can selfupdate
    Given nothing can selfupdate
    When I visit selfupdate
    Then I should receive 204 No Content
    Then I should see nothing

  Scenario: clientapp latest version has not published
    Given clientapp has version below:
      | version_code | version_name | status |
      | 10           | 1beta        | draft  |
    When I visit selfupdate
    Then I should receive 204 No Content
     And I should see nothing

  Scenario: some of clientapp versions are published
    Given clientapp has version below:
      | version_code | version_name | status |
      | 11           | 1beta        | draft  |
      | 21           | 2beta        | published  |
      | 32           | 3            | published  |
    When I visit selfupdate
    Then I should receive 200 OK
    Then I should receive client version code "32"
