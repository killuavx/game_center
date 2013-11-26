Feature: Add Package Bookmark
  As a Player
  I want to mark the package I interested
  So that I would love to keep in touch with the package

  Scenario: Failure to mark package without Sign in
    Given package title "Angry Birds" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

     When I mark package name "Angry Birds"
     Then I should receive 401 Unauthorized


  Scenario: Mark package successfully
    Given I sign in as "kent.back" already exists
    Given package title "Angry Birds" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

    Given package title "Minecraft" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 10           | 2013-10-10 23:21:00 |

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "0"

     When I mark package name "Angry Birds"
     Then I should receive 201 Created
      And I should see response with title "Angry Birds"

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "1"

     When I visit my bookmarks page
     Then I should receive 200 OK
      And I should see list result within pagination contains the title of element is "Angry Birds"


  Scenario: Mark multi package successfully
    Given I sign in as "kent.back" already exists
    Given package title "Angry Birds 2" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

    Given package title "Minecraft" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 4.0          | 4            | 2013-9-20 23:21:00 |

    When I visit my profile
    Then I should receive 200 OK
    And I should see response with bookmark_count "0"

    When I mark package name "Angry Birds 2"
    Then I should receive 201 Created

    When I mark package name "Minecraft"
    Then I should receive 201 Created

    When I visit my profile
    Then I should receive 200 OK
    And I should see response with bookmark_count "2"

    When I visit my bookmarks page
    Then I should receive 200 OK
    And I should see list result within pagination sequence like below:
      | title         |
      | Angry Birds 2 |
      | Minecraft     |
