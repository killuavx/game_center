@solrservice
@web
@webmob
@browser
Feature: Search Package

  Background:
    Given category tree exists
      And tipswords exists such below:
      | keyword | weight |
      | Speed   |   2    |
      | 消磨时间 |   1    |
      And package exists such below:
      | title                     | package_name              | categories                         | tags                    | released_datetime   |
      | 模拟人生3                   | com.eamobile             | 特色游戏, 大型游戏, 模拟经营          | 养成, 经典                | 2013-10-02 11:20:21 |
      | 古墓迷踪无限解锁版           | com.cwa.room              | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 破解, 解谜, 解锁          | 2013-10-01 11:20:21 |
      | 太空火箭兔解锁版             | com.Defiant.Rocket       | 特色游戏, 破解游戏, 休闲益智, 热门游戏 | 冒险, 破解, 解锁           | 2013-10-03 11:20:21 |
      | 火箭飞人无限金币版           | com.halpackj.amazon       | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 冒险, 破解, 解锁          | 2013-10-04 11:20:21 |
      | 小小盗贼全解锁版             | com.rovio.tiny           | 特色游戏, 破解游戏, 休闲益智          | 消磨时间, 破解, 解谜, 解锁  | 2013-10-05 11:20:21 |
      | 最终幻想：全员勇者  FFATB    | com.square.android.ffatb | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG                       | 2013-10-07 11:20:21 |
      | 极速狂徒无限金币版           | com.luko.car             | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度      | 2013-10-08 11:20:21 |
      | 武士大战僵尸直装无限金币版    | com.gluyd                | 特色游戏, 破解游戏, 动作射击          | 3D, 僵尸, 动作, 破解       | 2013-10-09 11:20:21 |
      | 捕鱼日记无限金币版           | com.fish                 | 特色游戏, 破解游戏, 精选游戏, 休闲益智 | 消磨时间, 解锁             |  2013-10-10 11:20:21 |
      | 保卫萝卜                   | com.carrot.carrotfantasy  | 特色游戏, 精选游戏, 休闲益智          | 消磨时间, 解锁             |  2013-10-10 11:20:21 |
      | 植物大战僵尸2高清版          | com.popcap.pvz2cthd360   | 特色游戏, 精选游戏, 休闲益智          | 消磨时间, 解锁             |  2013-10-10 11:20:21 |
     And rebuild searcher index

  Scenario: do Search and with search tags
    When I search with keyword "模拟"
    Then I should receive 200 OK
     And I should see "模拟人生3"

    When I press "消磨时间"
    Then I should receive 200 OK
     And I should see "捕鱼日记无限金币版"
     And I should see "保卫萝卜"
     And I should see "植物大战僵尸2高清版"


