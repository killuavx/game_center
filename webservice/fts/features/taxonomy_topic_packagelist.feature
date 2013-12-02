Feature: Topic
  As a Operator
  I want to add topic for package
  So that the topic can catch the players eye on some condition(special day or special event)

  Scenario: basic topic for package
    Given package exists such below:
      | title    | package_name | version_code | version_name |
      | 古墓迷踪  | com.cwa.room | 1            | 1.0          |
      | 天天酷跑  | com.enet.pao | 2            | 2.10         |
      And topic exists such below:
      | name    | slug             |
      | 大型游戏 | homebar-big-game |

      And topic slug "homebar-big-game" have own items such below:
      | content_type | object_field | object_value  | ordering |
      | package      | title        | 古墓迷踪       | 2        |
      | package      | title        | 天天酷跑       | 1        |

    When I visit topic detail page slug "homebar-big-game"
    Then I should receive 200 OK
     And I should see response with name "大型游戏"
     And I should see response with slug "homebar-big-game"
     And I should see response contains field "items_url"
    When I follow items_url on response
    Then I should receive 200 OK
     And I should see list result within pagination count equal "2"
     And I should see list result within pagination sequence like below:
      | title    |
      | 天天酷跑  |
      | 古墓迷踪  |

