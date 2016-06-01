Feature: Sign Out
  As a Game Center Player
  I want to Sign out in Game Center
  so that I can protected my account in idle.

  Scenario: Basic
    Given player "Kent.Back" already exists

     When I sign in as "kent.back"
     Then I should receive 200 OK

     When I sign out
     Then I should receive 200 OK

     When I visit my profile
     Then I should receive 401 UNAUTHORIZED

    