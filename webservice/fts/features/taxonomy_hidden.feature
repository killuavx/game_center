Feature: Hidden Category
  As Operator in Game Center
  I want to hide the category on the font side
  So that category cannot be visit through category list of font side
  but Identity url

  Scenario: new category
    Given the category "Big Game" as root just created
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

  Scenario: hide category and the category not found in category tree
    Given the category "Chinese Game" as root just created
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

    Given I hide the category
     When I visit category page
     Then I should receive 200 OK
      And I should see the category not in result tree

  Scenario: hide category but the category can be visit in the detial page
    Given the category "Chinese Game" as root just created
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

    Given I hide the category
     When I visit the category detail page
     Then I should receive 200 OK
      And I should see the category detail I just hidden
