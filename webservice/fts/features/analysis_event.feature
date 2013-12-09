Feature: collect user activated Event
  As a Operator
  I want to know how many/often people activated though event of client
  So that I can get to know platform status

  Scenario: Post New Event
    When I post event to analysis webservice on below:
      | eventtype | entrytype        | imei            |
      | activate  | client | 493002407599521 |
    Then I should receive 201 CREATED
     And I should see response with eventtype "activate"
     And I should see response with entrytype "client"
     And I should see response with imei "493002407599521"
     #And I should see response contains field "created_datetime"

  Scenario: Post New Event with signin
    Given I sign in as "kentback" already exists
    When I post event to analysis webservice on below:
      | eventtype | entrytype | imei            | package_name |
      | activate  | game      | 493002407599521 | com.fish     |
    Then I should receive 201 CREATED
     And I should see response with eventtype "activate"
     And I should see response with entrytype "game"
     And I should see response with imei "493002407599521"
