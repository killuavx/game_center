Feature: Sign Up Generically

  Scenario Outline: Success
    When I sign up with below information:
      | username      | password |
      | <signup_name> | 123455   |
    Then I should receive 201 CREATED
    And I should see response with username "<expect_name>"

  Examples: lower case
    | signup_name | expect_name |
    | martin      | martin      |

  Examples: complex case
    | signup_name | expect_name |
    | MaRTiN      | martin      |

  Scenario Outline: Fail
    When I sign up with below information:
      | username          | password          |
      | <signup_username> | <signup_password> |
    Then I should receive <status>
    And I should see "<message>"

    Examples: empty username
      | signup_username |  signup_password | status          | message |
      |                 |  1231            | 400 BAD REQUEST | Username should not be empty. |

    Examples: empty password
      | signup_username |  signup_password | status          | message |
      | kentback        |                  | 400 BAD REQUEST | Password should not be empty. |

  Scenario: Fail, username already taken
    When I sign up with below information:
      | username      | password |
      | Job           | 123455   |
    Then I should receive 201 CREATED

    When I sign up with below information:
      | username      | password |
      | job           | 654321   |
    Then I should receive 400 BAD REQUEST
     And I should see "This username is already taken."
