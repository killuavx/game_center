Feature: Topic list
  As a Operator
  I want to add topic for Choice Topic
  So that the topic can catch the players eye and categorized into Choice Topic

  @wip
  Scenario: top authors topic
    Given author "Gameloft" have package exists such below:
      | title           | package_name  | version_code | version_name |
      | 现代战争2黑色飞马 | ModernCombat2 |  1           | 1.0          |
      | 蜘蛛侠           | Spiderman     |  2           | 2.10         |
      And author "Kairosoft" have package exists such below:
      | title        | package_name                     | version_code | version_name |
      | 口袋学院      | net.kairosoft.android.school2_en |  3           | 1.0          |
      | 百货商店的故事 | net.kairosoft.android.depart_en  |  4           | 2.10         |

      And topic exists such below:
      | name    | slug              |
      | 精选专辑 | spec-choice-topic |
      And topic slug "spec-choice-topic" have own topic children such below:
      | name    | slug              |
      | 消磨时光 | topic-xiaomo      |
      | 狂野飙车 | topic-kuangye     |

      And topic slug "topic-xiaomo" have own items such below:
      | content_type | object_field | object_value  | ordering |
      | package      | title        | 口袋学院       | 2        |
      | package      | title        | 百货商店的故事  | 1        |

      And topic slug "topic-kuangye" have own items such below:
      | content_type | object_field | object_value   | ordering |
      | package      | title        | 现代战争2黑色飞马 | 2       |
      | package      | title        | 蜘蛛侠           | 1       |


    When I visit topic detail page slug "spec-choice-topic"
    Then I should receive 200 OK
     And I should see response with name "精选专辑"
     And I should see response with slug "spec-choice-topic"
     And I should see response contains field "children_url"
    When I follow children_url on response
    Then I should receive 200 OK
     And I should see list result within pagination count equal "2"
     And I should see list result within pagination sequence like below:
      | name    | slug          |
      | 消磨时光 | topic-xiaomo  |
      | 狂野飙车 | topic-kuangye |

    When I follow items_url of the element name "消磨时光" in list result of the response within pagination
    Then I should receive 200 OK
     And I should see list result within pagination count equal "2"
     And I should see list result within pagination sequence like below:
      | title        | package_name                     |
      | 百货商店的故事 | net.kairosoft.android.depart_en  |
      | 口袋学院      | net.kairosoft.android.school2_en |

