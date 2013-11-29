@wip
Feature: Search package
  As a player
  I want to search some app with keyword
  so that I can visit the app immediately

  Scenario: Empty
    When I search with keyword "nothing in warehouse"
    Then I should receive 200 OK
     And I should see empty list result within pagination

  Scenario: Search title
    Given category tree exists
      And package exists such below:
      | title                     | package_name              | categories                         | tags                    | released_datetime   |
      | 模拟人生3                   | com.eamobile             | 特色游戏, 大型游戏, 模拟经营          | 养成, 经典                | 2013-10-02 11:20:21 |
      | 古墓迷踪无限解锁版           | com.cwa.room              | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 破解, 解谜, 解锁          | 2013-10-01 11:20:21 |
      And rebuild searcher index

     When I search with keyword "模拟"
     Then I should receive 200 OK
      And I should see response with count "1"
      And I should see list result within pagination contains the title of element is "模拟人生3"

  Scenario: Search simple word
    Given category tree exists
      And package exists such below:
      | title                     | package_name              | categories                         | tags                    | released_datetime   |
      | 模拟人生3                   | com.eamobile             | 特色游戏, 大型游戏, 模拟经营          | 养成, 经典                | 2013-10-02 11:20:21 |
      | 古墓迷踪无限解锁版           | com.cwa.room              | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 破解, 解谜, 解锁          | 2013-10-01 11:20:21 |
      And rebuild searcher index

     When I search with keyword "模拟3"
     Then I should receive 200 OK
      And I should see response with count "1"
      And I should see list result within pagination contains the title of element is "模拟人生3"

  Scenario: revcive result more then one
    Given category tree exists
      And package exists such below:
      | title                     | package_name              | categories                         | tags                    | released_datetime   |
      | 太空火箭兔解锁版             | com.Defiant.Rocket       | 特色游戏, 破解游戏, 休闲益智, 热门游戏 | 冒险, 破解, 解锁           | 2013-10-03 11:20:21 |
      | 火箭飞人无限金币版           | com.halpackj.amazon       | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 冒险, 破解, 解锁          | 2013-10-04 11:20:21 |
      | 小小盗贼全解锁版             | com.rovio.tiny           | 特色游戏, 破解游戏, 休闲益智          | 消磨时间, 破解, 解谜, 解锁  | 2013-10-05 11:20:21 |
      And rebuild searcher index

     When I search with keyword "火箭"
     Then I should receive 200 OK
      And I should see response with count "2"
      And I should see list result within pagination contains the title of element is "火箭飞人无限金币版"
      And I should see list result within pagination contains the title of element is "太空火箭兔解锁版"

  Scenario: Search tags
    Given category tree exists
      And package exists such below:
      | title                     | package_name              | categories                         | tags                    | released_datetime   |
      | 最终幻想：全员勇者  FFATB    | com.square.android.ffatb | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG                       | 2013-10-07 11:20:21 |
      | 极速狂徒无限金币版           | com.luko.car             | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度      | 2013-10-08 11:20:21 |
      | 武士大战僵尸直装无限金币版    | com.gluyd                | 特色游戏, 破解游戏, 动作射击           | 3D, 僵尸, 动作, 破解       | 2013-10-09 11:20:21 |
      And rebuild searcher index

    When I search with keyword "3D"
    Then I should receive 200 OK
    And I should see response with count "1"
    And I should see list result within pagination contains the title of element is "武士大战僵尸直装无限金币版"

  Scenario: Search result sequence by -released_datetime
    Given category tree exists
      And package exists such below:
      | title                     | released_datetime | package_name  | categories                         | tags                    |
      | 最终幻想：全员勇者  FFATB    | 2013-10-01 11:23  | com.sq.ffatb  | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG                     |
      | 极速狂徒无限金币版           | 2013-10-01 11:23  | com.luko.car  | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度    |
      | 捕鱼日记无限金币版           | 2013-10-02 11:23  | com.fish      | 特色游戏, 破解游戏, 精选游戏, 休闲益智 | 消磨时间, 解锁            |
     And rebuild searcher index

    When I search with keyword "无限"
    Then I should receive 200 OK
    And I should see response with count "2"
    And I should see list result within pagination sequence like below:
      | title            | package_name  |
      | 捕鱼日记无限金币版  | com.fish      |
      | 极速狂徒无限金币版  | com.luko.car  |
