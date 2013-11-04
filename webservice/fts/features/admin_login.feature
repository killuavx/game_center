Feature: Login Admin

  As a Operator
  I want to login admin panel
  So that I can manage information of game center

  Background:
    Given a browser or client

  Scenario: Login Failure for User not exists
    When I login admin panel with username "admin" password "admin"
    Then I should not be logined to admin

  Scenario: Login Failure for password incurrect
    Given staff user exists below:
      | username | password     |
      | admin    | adminpass123 |
    When I login admin panel with username "admin" password "incurrect"
    Then I should not be logined to admin

  Scenario: Login Successful
    Given staff user exists below:
      | username | password     |
      | admin    | adminpass123 |
    When I login admin panel with username "admin" password "adminpass123"
    Then I should be logined to admin

