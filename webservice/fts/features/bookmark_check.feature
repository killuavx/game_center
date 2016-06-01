Feature: Check Package Bookmark

  Scenario: Failure to check bookmarks without Sign in
    Given package title "Angry Birds" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 2.0          | 2            | 2013-10-20 23:21:00 |

     When I check bookmark with package name "Angry Birds"
     Then I should receive 401 Unauthorized

  Scenario: Mark package successfully
    Given I sign in as "kent.back" already exists
    Given package title "Minecraft" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 10           | 2013-10-10 23:21:00 |

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with bookmark_count "0"

     When I check bookmark with package name "Minecraft"
     Then I should receive 404 NOT FOUND

     When I mark package name "Minecraft"
     Then I should receive 201 Created
      And I should see response with title "Minecraft"

     When I check bookmark with package name "Minecraft"
     Then I should receive 200 OK
