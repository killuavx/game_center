Feature: Sign Up Generically

  Scenario: Success
    When I am player, named "martin", email "martin@testcase.com", phone "+82-021-12345678", with password "123456"
    And I sign up with "martin"
    Then I should receive 201 CREATED
    And I should see player profile with named "martin", email "martin@testcase.com", phone "+82-021-12345678"

  Scenario Outline: Fail
    When I am player, named "<name>", email "<email>", phone "<phone>", with password "<password>"
    And I sign up with "<name>"
    Then I should receive <status>
    And I should see "<message>"

  Examples:
    | name      | email                  | phone            | password | status          | message |
    | kentback  | kentback@testcase.com  | +86-021-98213    | NONE     | 400 BAD REQUEST | password should not be empty |
    | uncle.bob | uncle.bob@testcase.com | NONE             | 1234567  | 400 BAD REQUEST | phone should not be empty  |
    | mike      | NONE                   | +86-021-23211457 | 1234567  | 400 BAD REQUEST | email should not be empty  |

