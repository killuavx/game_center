Feature: show Advertisement
  As a Operator
  I want to Advertising
  So that I can promote more interesting game

  Scenario: Visit Forbidden
    When I visit advertisements with no place
    Then I should receive 403 FORBIDDEN

  Scenario: one advertisement
    Given place "home-recommend-game" exists
    Given package exists such below:
      | title     | package_name    | version_code | version_name |
      | 愤怒的小鸟 | com.rovio.angry |  1           | 1.0          |
      And advertisement exists on place "home-recommend-game" with content on below:
      | title        | content_type | object_field | object_value    |
      | 小鸟的愤怒登场 | package      | package_name | com.rovio.angry |

    When I visit advertisements on place "home-recommend-game"
    Then I should receive 200 OK
     And I should see response with count "1"
     And I should see list result within pagination contains the title of element is "小鸟的愤怒登场"

    When I follow content_url of the element title "小鸟的愤怒登场" in list result of the response within pagination
    Then I should receive 200 OK
     And I should see response with title "愤怒的小鸟"

  Scenario: advertisement list on one place
    Given place "home-recommend-game" exists
    Given package exists such below:
      | title     | package_name    | version_code | version_name |
      | 愤怒的小鸟 | com.rovio.angry |  1           | 1.0          |
      | 极品飞车12  | com.speed        |  12           | 12.0          |
    And advertisement exists on place "home-recommend-game" with content on below:
      | title        | content_type | object_field | object_value    |
      | 小鸟的愤怒登场 | package      | package_name | com.rovio.angry |
      | 极品12速递    | package      | package_name | com.speed       |

    When I visit advertisements on place "home-recommend-game"
    Then I should receive 200 OK
     And I should see response with count "2"
     And I should see list result within pagination contains the title of element is "小鸟的愤怒登场"
     And I should see list result within pagination contains the title of element is "极品12速递"

  Scenario: advertisement list on one place
    Given place "home-recommend-game" exists
    Given package exists such below:
      | title     | package_name    | version_code | version_name |
      | 愤怒的小鸟 | com.rovio.angry  |  1           | 1.0          |
      | 极品飞车12 | com.speed       |  12           | 12.0          |
    And advertisement exists on place "home-recommend-game" with content on below:
      | title        | content_type | object_field | object_value    | ordering |
      | 极品12速递    | package      | package_name | com.speed       | 1        |
      | 小鸟的愤怒登场 | package      | package_name | com.rovio.angry | 2        |

    When I visit advertisements on place "home-recommend-game"
    Then I should receive 200 OK
    And I should see response with count "2"
    And I should see list result within pagination sequence like below:
      | title        |
      | 小鸟的愤怒登场 |
      | 极品12速递    |

  Scenario: advertisement list on difference places
    Given place "home-network-game" exists
    Given place "home-recommend-game" exists
    Given package exists such below:
      | title     | package_name    | version_code | version_name |
      | 愤怒的小鸟 | com.rovio.angry |  1           | 1.0          |
      | 极品飞车12 | com.speed       |  12          | 12.0         |
      | 古墓迷踪   | com.cwa.room    | 1            | 1.0          |
      | 天天酷跑   | com.enet.pao    | 2            | 1.10         |
      And advertisement exists on place "home-recommend-game" with content on below:
      | title        | content_type | object_field | object_value    | ordering |
      | 极品12速递    | package      | package_name | com.speed       | 1        |
      | 小鸟的愤怒登场 | package      | package_name | com.rovio.angry | 2        |
      And advertisement exists on place "home-network-game" with content on below:
      | title        | content_type | object_field | object_value    | ordering |
      | 极品12速递    | package      | package_name | com.speed       | 2        |
      | 古墓迷踪      | package      | package_name | com.cwa.room    | 3        |
      | 天天酷跑      | package      | package_name | com.enet.pao    | 1        |

     When I visit advertisements on place "home-recommend-game"
     Then I should receive 200 OK
      And I should see response with count "2"
      And I should see list result within pagination sequence like below:
      | title        |
      | 小鸟的愤怒登场 |
      | 极品12速递    |

     When I visit advertisements on place "home-network-game"
     Then I should receive 200 OK
      And I should see response with count "3"
      And I should see list result within pagination sequence like below:
      | title        |
      | 古墓迷踪      |
      | 极品12速递    |
      | 天天酷跑      |
