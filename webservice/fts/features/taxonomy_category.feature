Feature: Category and package list by category
  As a Operator
  I want to categoried all packages
  So that I can manage package easily and guiding player to find package by category clearly

  Scenario: new category
    Given category "Big Game" as root already exists
      And I focus on category "Big Game"
     When I visit category page
     Then I should receive 200 OK
      And I should see the category in result tree

  Scenario: visit package list by category
    Given category tree exists
      And package exists such below:
      | title                     | released_datetime | package_name  | categories                         |
      | 最终幻想：全员勇者  FFATB    | 2013-10-01 11:23  | com.sq.ffatb  | 特色游戏, 破解游戏, 角色扮演, 最新游戏 |
      | 极速狂徒无限金币版           | 2013-10-02 11:23  | com.luko.car  | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 |
      | 捕鱼日记无限金币版           | 2013-10-03 11:23  | com.fish      | 特色游戏, 破解游戏, 精选游戏, 休闲益智 |

     When I visit package list of category name "特色游戏"
     Then I should receive 200 OK
      And I should see response with count "3"
      And I should see list result within pagination sequence like below:
      | title                   | package_name  |
      | 捕鱼日记无限金币版         | com.fish      |
      | 极速狂徒无限金币版         | com.luko.car  |
      | 最终幻想：全员勇者  FFATB  | com.sq.ffatb  |

    When I visit package list of category name "精选游戏"
    Then I should receive 200 OK
    And I should see response with count "2"
    And I should see list result within pagination sequence like below:
      | title           | package_name  |
      | 捕鱼日记无限金币版 | com.fish      |
      | 极速狂徒无限金币版 | com.luko.car  |


