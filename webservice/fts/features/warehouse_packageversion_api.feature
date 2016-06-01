Feature: Visit Package Version
  As a player
  I want to find more version
  So that I can play hat I had interested in

  Scenario: No other version
    Given package name "com.rovio.angrybirdsrio" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.0          | 1            | 2013-8-29 12:11   |
      And I focus on package name "com.rovio.angrybirdsrio" version code "1"

     When I visit the package detail
     Then I should receive 200 OK
      And I should see response contains field "versions_url"

     When I follow the package versions_url
     Then I should receive 200 OK
      And I should see list result within pagination count equal "1"
      And I should see list result within pagination contains the version_name of element is "1.0"


  Scenario: normal version list sort by -version_code
    Given package name "com.tencent.pao" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.0          | 1            | 2013-8-29 12:11   |
      | 2.0beta      | 2            | 2013-9-29 12:11   |
      | 3.0          | 3            | 2013-10-29 12:11  |
    And I focus on package name "com.tencent.pao" version code "1"

    When I visit the package detail
    Then I should receive 200 OK
    And I should see response contains field "versions_url"

    When I follow the package versions_url
    Then I should receive 200 OK
     And I should see list result within pagination count equal "3"
     And I should see list result within pagination sequence like below:
       | version_name | version_code |
       | 3.0          | 3            |
       | 2.0beta      | 2            |
       | 1.0          | 1            |


  Scenario: version list limit by 10
    Given package name "com.tencent.pao" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.0          | 1            | 2013-1-29 12:11   |
      | 2.0beta      | 2            | 2013-2-28 12:11   |
      | 3.0          | 3            | 2013-3-29 12:11   |
      | 4.0          | 4            | 2013-4-29 12:11   |
      | 5.0          | 5            | 2013-5-29 12:11   |
      | 6.0          | 6            | 2013-6-29 12:11   |
      | 7.0          | 7            | 2013-7-29 12:11   |
      | 8.0          | 8            | 2013-8-29 12:11   |
      | 9.0          | 9            | 2013-9-29 12:11   |
      | 10.0         | 10           | 2013-10-29 12:11  |
      | 11.0         | 11           | 2013-11-10 12:11  |
    And I focus on package name "com.tencent.pao" version code "1"

    When I visit the package detail
    Then I should receive 200 OK
    And I should see response contains field "versions_url"

    When I follow the package versions_url
    Then I should receive 200 OK
     And I should see list result within pagination count equal "11"
     And I should see list result within pagination have 10 elements

  Scenario: version list limit by 10
    Given package name "com.tencent.pao" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 1.0          | 1            | 2013-1-29 12:11   |
      | 2.0beta      | 2            | 2013-2-28 12:11   |

    Given package name "com.rovio.angrybirdsrio" has a set of versions below:
      | version_name | version_code | released_datetime |
      | 8.0         | 10           | 2013-10-29 12:11  |
    And I focus on package name "com.rovio.angrybirdsrio" version code "10"

    When I visit the package detail
    Then I should receive 200 OK
    And I should see response contains field "versions_url"

    When I follow the package versions_url
    Then I should receive 200 OK
    And I should see list result within pagination count equal "1"
    And I should see list result within pagination have 1 elements
