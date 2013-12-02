Feature: Package detail
  As a Player
  I want to see more information about the package
  So that I can choose which game to download and play

  Scenario: detail information
    Given category tree exists
      And package exists such below:
      | title                      | package_name             | categories                        | tags         | version_code | version_name |
      | 愤怒的小鸟：星球大战无限道具版 | com.rovio.angry.ads.iap  | 特色游戏, 破解游戏, 休闲益智, 热门游戏 | 消磨时间, 解锁 | 1            | 1.0          |
      And I focus on package title "愤怒的小鸟：星球大战无限道具版"

    When I visit the package detail
    Then I should receive 200 OK

    # basic information
     And I should see response with title "愤怒的小鸟：星球大战无限道具版"
     And I should see response with package_name "com.rovio.angry.ads.iap"

    # latest version information
     And I should see response with version_code "1"
     And I should see response with version_name "1.0"

    # taxonomy information
     And I should see response with category_name "特色游戏"
     And I should see response contains with categories_names on below:
      | value   |
      | 特色游戏 |
      | 破解游戏 |
      | 休闲益智 |
      | 热门游戏 |
     And I should see response contains with tags on below:
      | value   |
      | 消磨时间 |
      | 解锁    |

  Scenario: another information
    Given category tree exists
      And package exists such below:
        | title    | package_name      | categories | version_code | version_name |
        | 愤怒的小鸟 | com.rovio.angry  | 特色游戏     | 1            | 1.0          |
      And I focus on package title "愤怒的小鸟"

     When I visit the package detail
     Then I should receive 200 OK

      And I should see response contains field "icon"
      And I should see response contains field "cover"
      And I should see response contains field "whatsnew"
      And I should see response contains field "summary"
      And I should see response contains field "description"
      And I should see response contains field "comments_url"
      And I should see response contains field "author"
      And I should see response contains field "released_datetime"
      And I should see response contains field "versions_url"
      And I should see response contains field "related_packages_url"
      And I should see response contains field "download"
      And I should see response contains field "download_size"
      And I should see response contains field "download_count"

  @wip
  Scenario: download with data integration
    Given category tree exists
      And package exists such below:
      | title    | package_name     | categories | version_code | version_name | download |
      | 愤怒的小鸟 | com.rovio.angry | 特色游戏     | 1            | 1.0          |          |
      And I focus on package title "愤怒的小鸟"

     When I visit the package detail
     Then I should receive 200 OK
     And I should see response field download endswith ".apk"

    Given change download of the package version to cpk

     When I visit the package detail
     Then I should receive 200 OK
      And I should see response field download endswith ".cpk"

