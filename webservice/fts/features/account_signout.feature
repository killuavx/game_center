Feature: Sign Out
  As a Game Center Player
  I want to Sign out in Game Center
  so that I can protected my account in idle.

  Scenario: Basic
    Given I am player in game center, , named "martin", email "martin@testcase.com", phone "+86-021-12345678", with password "123456"
    When I sign in as "martin" with email
    Then I should receive 200 OK
    And I should see my authorization token
    When I sign out as "martin"
    Then I should receive 200 OK
    When I visit my profile using my authorization token
    Then I should receive 401 UNAUTHORIZED

    