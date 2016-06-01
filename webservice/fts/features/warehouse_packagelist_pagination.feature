Feature: package list paginate
  As a player
  I want to receive package list by paginate by custom
  So that I can see difference view between application and game list

  Background:
    Given a browser or client
      And category tree exists
      And package exists such below:
      | title                     | package_name              | categories                         | tags                     | version_name | version_code | released_datetime |
      | 古墓迷踪无限解锁版           | com.cwa.room              | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 破解, 解谜, 解锁           | 1.0          | 1 | 2013-10-01 11:20:21 |
      | 太空火箭兔解锁版             | com.Defiant.Rocket       | 特色游戏, 破解游戏, 休闲益智, 热门游戏 | 冒险, 破解, 解锁           | 1.0          | 1 | 2013-10-02 11:20:21 |
      | 小小盗贼全解锁版             | com.rovio.tiny           | 特色游戏, 破解游戏, 休闲益智          | 消磨时间, 破解, 解谜, 解锁   | 1.0          | 1 | 2013-10-03 11:20:21 |
      | 希曼                       | com.chill.android.row    | 特色游戏, 大型游戏, 角色扮演          | 动作, 怀旧, 经典, 闯关       | 1.0          | 1 | 2013-10-04 11:20:21 |
      | 愤怒的小鸟：星球大战无限道具版 | com.rovio.angry.ads.iap  | 特色游戏, 破解游戏, 休闲益智, 热门游戏 | 消磨时间, 解锁              | 1.0          | 1 | 2013-10-05 11:20:21 |
      | 捕鱼日记无限金币版           | com.fish                 | 特色游戏, 破解游戏, 精选游戏, 休闲益智 | 消磨时间, 解锁             | 1.0          | 1 | 2013-10-06 11:20:21 |
      | 最终幻想：全员勇者  FFATB    | com.square.android.ffatb | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG                      | 1.0           | 1 | 2013-10-07 11:20:21 |
      | 极速狂徒无限金币版           | com.luko.car             | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度      | 1.0          | 1 | 2013-10-08 11:20:21 |
      | 模拟人生3                   | com.eamobile             | 特色游戏, 大型游戏, 模拟经营          | 养成, 经典                 | 1.0          | 1 | 2013-10-09 11:20:21 |
      | 武士大战僵尸直装无限金币版    | com.gluyd                | 特色游戏, 破解游戏, 动作射击           | 3D, 僵尸, 动作, 破解       | 1.0          | 1 | 2013-10-10 11:20:21 |
      | 极速狂徒无限金币版           | com.lcar                  | 特色游戏, 破解游戏, 精选游戏, 赛车竞速 | 激情, 解锁, 赛车, 速度 | 1.0 | 1 | 2013-10-11 12:01:45 |
      | 火箭飞人无限金币版           | com.halpackj.amazon       | 特色游戏, 破解游戏, 中文游戏, 休闲益智 | 冒险, 破解, 解锁 | 1.0 | 1 | 2013-10-11 12:01:45 |
      | 鳄鱼小顽皮爱洗澡2破解版      | com.dismywater2           | 特色游戏, 精选游戏, 休闲益智, 热门游戏, 最新游戏 | 可爱, 破解, 解谜 | 1.0 | 1 | 2013-10-11 12:01:45 |
      | 麻将探险之旅                | com.vaxij                 | 特色游戏, 棋牌游戏, 最新游戏          | 桌游, 棋牌, 闯关 | 1.0 | 1 | 2013-10-11 12:01:45 |
      | 最终幻想：全员勇者  FFATB    | com.squeiday.fab          | 特色游戏, 破解游戏, 角色扮演, 最新游戏 | RPG | 1.0 | 1 | 2013-10-11 12:01:45 |
      | 涂鸦英雄                   | com.mvn.screhero1          | 特色游戏, 动作射击                  | TD, 塔防, 策略 | 1.0 | 1 | 2013-10-11 12:01:45 |

  Scenario: default list paginate by 10 items
    When I visit package list of category name "特色游戏"
    Then I should see list result within pagination count equal "16"
     And I should see list result within pagination paginate by "10" items

  Scenario: list paginate by custom size
    When I visit package list of category name "特色游戏" paginate by "16"
    Then I should see list result within pagination count equal "16"
    And I should see list result within pagination paginate by "16" items
