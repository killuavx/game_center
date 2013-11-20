Feature: Package Update
  As a Game Center Mobile Player
  I want to receive package update notices from webservice
  so that I can install and play new game in time.

  Background: Packages
    Given package exists such below:
      | title            | package_name               | version_name | version_code | released_datetime |
      | 保卫萝卜          | com.carrot.carrotfantasy   | 1.1.1        | 258          |  2013-8-29 12:11  |
      | 游戏存档-j子      | com.lion.backups           | 1.0         | 1             |  2013-9-08 12:11  |
      | 植物大战僵尸2高清版 | com.popcap.pvz2cthd360     | 1.0.1       | 1             |  2013-8-29 12:11 |
      | 齐B小短裙         | com.racttoy.qbxdq.activity | 1.0         | 1             |  2013-8-29 12:11  |
      | 天天酷跑          | com.tencent.pao            | 1.0.6.0     | 10            |  2013-8-29 12:11  |

  Scenario Outline: update
    Given package name "<package_name>" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.1.2beta    | 259          | 2013-8-29 12:11   |
      | 1.2.1        | 268          | 2013-8-30 12:11   |
     And I focus on package name "<package_name>"
    When I post package version to check update with package_name: "<package_name>", version_name: "<version_name>", version_code: "<version_code>"
    Then I should receive 200 OK
    Then I should see package update list has the version package_name: "<package_name>", version_name: "<response_version_name>", version_code: "<response_version_code>", it can <is_updatable> update

    Examples: can be update, in package versions range
      | package_name             | version_name | version_code | response_version_name | response_version_code | is_updatable |
      | com.carrot.carrotfantasy | 1.1.1        | 258          | 1.2.1                 | 268                   | be |

    Examples: can be update, out of package versions range
      | package_name             | version_name | version_code | response_version_name | response_version_code | is_updatable |
      | com.carrot.carrotfantasy | 1.0.0        | 218          | 1.2.1                 | 268                   | be     |

  Scenario Outline: ignore update
    Given package name "<package_name>" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.1.2beta    | 259          | 2013-8-29 12:11   |
      | 1.2.1        | 268          | 2013-8-30 12:11   |
    When I post package version to check update with package_name: "<package_name>", version_name: "<version_name>", version_code: "<version_code>"
    Then I should receive 200 OK
    Then I should see empty package update list

    Examples: can not be update, in package versions range
      | package_name             | version_name | version_code |
      | com.carrot.carrotfantasy | 1.2.1        | 268          |

    Examples: can not be update, out of package versions range
      | package_name             | version_name | version_code |
      | com.carrot.carrotfantasy | 2.1.1        | 358          |
