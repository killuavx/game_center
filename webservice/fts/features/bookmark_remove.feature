Feature: Unmark Package
  As a Player
  I want to unmark package not interested any more
  So that I can ignore the package

  Scenario: Failure to unmark package without Sign in
    Given package title "Angry Birds" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

    When I unmark package name "Angry Birds"
    Then I should receive 401 Unauthorized

  Scenario: Mark/Unmark package successfully
    Given I sign in as "kent.back" already exists
    Given package title "Angry Birds 2" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "0"

     When I mark package name "Angry Birds 2"
     Then I should receive 201 Created

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "1"

     When I visit my bookmarks page
     Then I should receive 200 OK
      And I should see list result within pagination sequence like below:
        | title         |
        | Angry Birds 2 |

     When I unmark package name "Angry Birds 2"
     Then I should receive 204 No Content

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "0"

     When I visit my bookmarks page
     Then I should receive 200 OK
     And I should see empty list result within pagination

