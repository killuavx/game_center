Feature: Sort tipsword
  As a Operator
  I want to sort tipsworld order by weight
  So that the top keyword will guiding user's attention on some related applications

  Scenario: sort with weight
    Given tipswords exists such below:
      | keyword | weight |
      | Speed   |   2    |
      | network |   4    |
      | 3D      |   1    |
    When I visit tipswords page
    Then I should receive 200 OK
    And I should see list result within pagination count equal "3"
    And I should see list result within pagination sequence like below:
      | keyword | weight |
      | network |   4    |
      | Speed   |   2    |
      | 3D      |   1    |
