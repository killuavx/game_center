@web
@webmob
@browser
Feature: Search Package

  Background:
    Given category tree exists
      And package exists such below:
      | title                   | package_name             | categories                         | tags                    | released_datetime   |
      | 模拟人生3                | com.eamobile             | 特色游戏, 大型游戏, 模拟经营          | 养成, 经典                | 2013-10-02 11:20:21 |
      | 最终幻想：全员勇者  FFATB | com.square.android.ffatb | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG                       | 2013-10-07 11:20:21 |
      | 极速狂徒无限金币版        | com.luko.car             | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度      | 2013-10-08 11:20:21 |

  Scenario: do Search and with search tags
    When I search with keyword "模拟"
    Then I should receive 200 OK
    And I should see "模拟人生3"

    When I press "消磨时间"
    Then I should receive 200 OK
    And I should see "捕鱼日记无限金币版"
    And I should see "保卫萝卜"
    And I should see "植物大战僵尸2高清版"

