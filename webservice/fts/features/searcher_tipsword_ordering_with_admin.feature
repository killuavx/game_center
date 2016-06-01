Feature: Sort tipsword
  As a Operator
  I want to sort tipsworld order by weight
  So that the top keyword will guiding user's attention on some related applications

  @browser
  Scenario: sort with weight on admin panel
    Given a browser or client
      And login admin as supperuser "admin" already exists
     When I visit tipsword create page
      And I create tipswords below:
       | keyword |
       | Relax   |
       | Action  |
       | Sports  |

    When I visit tipswords page
    Then I should receive 200 OK
     And I should see list result within pagination count equal "3"
     And I should see list result within pagination sequence like below:
       | keyword | weight |
       | Sports  |   3    |
       | Action  |   2    |
       | Relax   |   1    |

    When I visit tipsword list page
     #And I move row contains "Sports" up 3 times
     And I fill row contains "Relax" in name "weight" with "10"
     And I press "_save"
    Then I should receive 200 OK

    When I visit tipswords page
    Then I should receive 200 OK
     And I should see list result within pagination count equal "3"
     And I should see list result within pagination sequence like below:
       | keyword | weight |
       | Relax   |   10   |
       | Sports  |   3    |
       | Action  |   2    |

