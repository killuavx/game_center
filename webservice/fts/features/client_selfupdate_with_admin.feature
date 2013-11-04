Feature: update client
  As a Operator
  I want to manage client version on game center
  So that I can notify ccplay user in client to selfupdate

  Background:
    Given a browser or client
      And login admin as supperuser "admin" already exists

  Scenario: clientapp latest version has not published
    When I create client version below:
      | version_code | version_name | status |
      | 10           | 1beta        | draft  |
    When I visit selfupdate
    Then I should receive 204 No Content

  @browser
  Scenario: some of clientapp versions are published
    When I create client version below:
      | version_code | version_name | status     | whatsnew | summary |
      | 11           | 1beta        | published  | initial version | Hello World |
      | 21           | 2beta        | draft      | just debug |  debug version |
      | 32           | 3            | published  | basic function | have a nice day |
    When I visit selfupdate
    Then I should receive 200 OK
     And I should receive client package version version_code "32"
     And I should receive client package version whatsnew "basic function"
     And I should receive client package version summary "have a nice day"
