Feature: Hidden Category
  As a Operator
  I want to hide the category on the font side
  So that category cannot be visit through category list of font side but Identity url

  Scenario: hide category and the category not found in category tree
    Given category "Chinese Game" as root already exists
      And I focus on category "Chinese Game"
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

    Given I hide the category
     When I visit category page
     Then I should receive 200 OK
      And I should see the category not in result tree

  Scenario: hide category but the category can be visit in the detial page
    Given category "Chinese Game" as root already exists
      And I focus on category "Chinese Game"
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

    Given I hide the category
     When I visit the category detail page
     Then I should receive 200 OK
      And I should see response with name "Chinese Game"
