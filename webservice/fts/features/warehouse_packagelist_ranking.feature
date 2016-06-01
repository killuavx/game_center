Feature: Ranking List
  As a Player
  I want to know what top10 games are
  So that I can try to play game in top10 ranking

  Scenario: simple list order by package version total download_count
    Given category tree exists
      And package exists such below:
      | title   | package_name  | version_code | version_name | download_count |
      | 古墓迷踪 | com.cwa.room  | 1            | 1.0          | 10             |
      | 模拟人生3| com.eamobil   | 1            | 1.0          | 21             |

      # 模拟人生3 total download_count 21
      # 古墓迷踪  total download_count 22 = 10+12,
      And package title "古墓迷踪" has a set of versions below:
      | version_code | version_name | download_count |
      | 2            | 2.0          | 12             |

     When I visit ranking list page
     Then I should receive 200 OK
      And I should see response with count "2"
      And I should see list result within pagination sequence like below:
      | title   | package_name  |
      | 古墓迷踪 | com.cwa.room  |
      | 模拟人生3| com.eamobil   |

  Scenario: simple list exclude package of application category
    Given category tree exists
    And package exists such below:
      | title   | package_name    | categories | version_code | version_name | download_count |
      | 古墓迷踪 | com.cwa.room    | 破解游戏    | 1            | 1.0          | 10             |
      | 模拟人生3| com.eamobil     | 特色游戏    | 1            | 1.0          | 21             |
      | 应用管家 | com.app.manager | 装机必备    | 1            | 1.0          | 11             |

    When I visit ranking list page
    Then I should receive 200 OK
    And I should see response with count "2"
    And I should see list result within pagination sequence like below:
      | title   | package_name  |
      | 模拟人生3| com.eamobil   |
      | 古墓迷踪 | com.cwa.room  |
