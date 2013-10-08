Feature: Sign In and Visit profile myself
  As a Game Center Player
  I want to Sign in Game Center with my email or phone
  so that I can visit my profile and take part in another activities.

  Background:
    Given I am player in game center, named "martin", email "martin@testcase.com", phone "+86-021-12345678", with password "123456"

  @web @noui
  Scenario Outline: Sign In
    When I sign in as "martin" with email
    Then I should receive 200 OK
    And I should see my authorization token
    When I visit my profile using my authorization token
    Then I should receive 200 OK
    And I should see player profile with named "martin", email "martin@testcase.com", phone "+86-021-12345678"

    Examples: email Sign in
      | signin_type | signin_value |
      | email       | martin@testcase.com |

    Examples: phone Sign in
      | signin_type | signin_value |
      | phone       | +86-021-12345678 |
