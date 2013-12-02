Feature: Top Authors Topic
  As a Operator
  I want to add topic for author
  So that the topic can catch the players eye on top authors

  Scenario: top authors topic
    Given author "Gameloft" have package exists such below:
      | title           | package_name  | version_code | version_name |
      | 现代战争2黑色飞马 | ModernCombat2 |  1           | 1.0          |
      | 蜘蛛侠           | Spiderman     |  2           | 2.10         |
      And author "Kairosoft" have package exists such below:
      | title        | package_name                     | released_datetime | version_code | version_name |
      | 口袋学院      | net.kairosoft.android.school2_en | 2013-11-02 11:21  | 3           | 1.0          |
      | 百货商店的故事 | net.kairosoft.android.depart_en  | 2013-11-01 11:21  | 4           | 2.10         |

      And topic exists such below:
      | name     | slug             |
      | 顶级开发商 | spec-top-author |
      And topic slug "spec-top-author" have own items such below:
      | content_type | object_field | object_value  | ordering |
      | author       | name         | Gameloft      | 2        |
      | author       | name         | Kairosoft     | 1        |

    When I visit topic detail page slug "spec-top-author"
    Then I should receive 200 OK
     And I should see response with name "顶级开发商"
     And I should see response with slug "spec-top-author"
     And I should see response contains field "items_url"
    When I follow items_url on response
    Then I should receive 200 OK
     And I should see list result within pagination count equal "2"
     And I should see list result within pagination sequence like below:
      | name      |
      | Kairosoft |
      | Gameloft  |

    When I follow packages_url of the element name "Kairosoft" in list result of the response within pagination
    Then I should receive 200 OK
     And I should see list result within pagination count equal "2"
     And I should see list result within pagination sequence like below:
      | title        | package_name                     |
      | 口袋学院      | net.kairosoft.android.school2_en |
      | 百货商店的故事 | net.kairosoft.android.depart_en  |

