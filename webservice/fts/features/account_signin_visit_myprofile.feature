@restapi
Feature: Sign In and Visit profile myself
  As a Game Center Player
  I want to Sign in Game Center with my email or phone
  so that I can visit my profile and take part in another activities.

  Background:
    Given player "Uncle.Rob" already exists

  Scenario Outline: Sign In
    When I sign in as "<signin_username>"
    Then I should receive 200 OK
    When I visit my profile
    Then I should receive 200 OK
     And I should see response with username "<profile_username>"

    Examples: sign in case-insensitive
      | signin_username | profile_username |
      | uncle.rob       | uncle.rob        |
      | Uncle.Rob       | uncle.rob        |

