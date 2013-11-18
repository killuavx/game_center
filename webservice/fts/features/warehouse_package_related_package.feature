Feature: Package Related Other Packages
  As a player
  I want to know what any package does similar to the package I watching on detail
  So that I can find more different packages

  Background:
    Given a browser or client

  Scenario Outline: related nothing
    Given category tree exists
      And package exists such below:
      | title            | package_name           | categories    | tags | version_name | version_code | status    |
      | 植物大战僵尸2高清版 | com.popcap.pvz2cthd360 | <pkg_a_cats> |  <pkg_a_tags>  | 1.0.1       | 1    | published |
      | Angry Birds Rio  | com.rovio.angrybirdsrio |  <pkg_b_cats> | <pkg_b_tags> | 1.0      | 10      | published |

    Examples: Different Category
      | pkg_a_cats          | pkg_b_cats       | pkg_a_tags | pkg_b_tags |
      | crack-game,big-game | stand-alone-game | hot        | hot        |

    Examples: Different Tag
      | pkg_a_cats          | pkg_b_cats                | pkg_a_tags | pkg_b_tags |
      | crack-game,big-game | big-game,stand-alone-game | cartoon   |  aag   |

    Given I focus on package title "Angry Birds Rio"
     When I visit the package detail
      And I follow the package related_packages_url
     Then I should receive 200 OK
      And I should see empty list result within pagination

  Scenario Outline: some related packages
    Given category tree exists
      And package exists such below:
      | title            | package_name            | categories    | tags         | version_name | version_code | status    |
      | 捕鱼达人          | com.huayigame.fkdy      | <pkg_a_cats>  | <pkg_a_tags> | 1.0.1        | 1            | published |
      | Angry Birds Rio  | com.rovio.angrybirdsrio | <pkg_b_cats>  | <pkg_b_tags> | 1.0          | 10           | published |
      And I focus on package title "Angry Birds Rio"

    When I visit the package detail
     And I follow the package related_packages_url
    Then I should receive 200 OK
     And I should see list result within pagination count equal "1"
     And I should see list result within pagination contains the title of element is "捕鱼达人"

    Examples: same category
      | pkg_a_cats                  | pkg_b_cats                | pkg_a_tags | pkg_b_tags |
      | stand-alone-game,big-game   | stand-alone-game          | cn,cute    | hot,cute   |

    Examples: multi-category
      | pkg_a_cats                  | pkg_b_cats                | pkg_a_tags | pkg_b_tags |
      | stand-alone-game,crack-game | big-game,stand-alone-game | cn,cartoon | cn,cartoon |

  Scenario Outline: some related packages with multi-version
    Given category tree exists
      And package exists such below:
      | title            | package_name            | categories    | tags         | version_name | version_code | status    |
      | 捕鱼达人          | com.huayigame.fkdy      | <pkg_a_cats>  | <pkg_a_tags> | 1.0.1        | 1            | published |
      | 捕鱼达人          | com.huayigame.fkdy      | <pkg_a_cats>  | <pkg_a_tags> | 2.0.1        | 2            | published |
      | Angry Birds Rio  | com.rovio.angrybirdsrio | <pkg_b_cats>  | <pkg_b_tags> | 1.0          | 10           | published |
      And I focus on package title "Angry Birds Rio"

    When I visit the package detail
    And I follow the package related_packages_url
    Then I should receive 200 OK
    And I should see list result within pagination count equal "1"
    And I should see list result within pagination contains the title of element is "捕鱼达人"

  Examples: same multi-category
      | pkg_a_cats                  | pkg_b_cats                | pkg_a_tags | pkg_b_tags |
      | stand-alone-game,big-game   | stand-alone-game,big-game | cn,cute    | hot,cute   |
