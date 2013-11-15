Feature: post comment to package version
  As a Player
  I want to post comment to package version
  So that I can suggest some idea for the game

  Scenario: post comment require sign in before
    Given package name "call me MT" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |

    When I post comment "great job" to the package title "call me MT" version_code "1"
    Then I should receive 401 Unauthorized

  Scenario: Empty Comment
    Given package name "call me MT" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |
    Given post comment status of platform default is unpublished

    When I visit the package detail title "call me MT"
    Then I should receive 200 OK
     And I should see comment_count 0 in the package version detail

    When I visit comment list of the package version
    Then I should receive 200 OK

  Scenario Outline: Post Comment and set status published/unpublished

    Given I sign in as player name "fox20century" exists in game center
    Given package name "<title>" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |
    Given post comment status of platform default is unpublished

    When I post comment "great job" to the package title "<title>" version_code "<version_code>"
    Then I should receive 201 Created
     And I should see response with comment "great job"

    # new comment is_public = False
    When I visit the package detail title "<title>"
    Then I should receive 200 OK
     And I should see comment_count 0 in the package version detail

    # set comment is_public = True
    Given the comment of package name "call me MT" version_code "1" change to published
     When I visit the package detail title "<title>"
     Then I should receive 200 OK
      And I should see comment_count 1 in the package version detail

     When I visit comment list of the package version
     Then I should receive 200 OK
      And I should see list result within pagination contains the comment of element is "great job"

     When I visit my profile
     Then I should receive 200 OK
      And I should see response with comment_count "1"

     When I visit my commented package page
     Then I should receive 200 OK
      # I should see the package commented by me in result list
      And I should see list result within pagination contains the title of element is "<title>"

    # set comment is_public = False
    Given the comment of package name "call me MT" version_code "1" change to unpublished
     When I visit the package detail title "<title>"
     Then I should receive 200 OK
      And I should see comment_count 0 in the package version detail

    Examples:
      | title      | version_code |
      | call me MT | 1            |
