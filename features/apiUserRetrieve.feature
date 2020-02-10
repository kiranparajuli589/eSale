Feature: retrieve created users

  Background:
    Given following users have been created with default attributes
      | username | email          | password    |
      | user0    | user0@test.com | #uu0?test12 |
      | user1    | user1@test.com | #uu1?test12 |

  Scenario: retrieve a valid user using rest-api
    When admin sends a get request to retrieve all users
    Then users with following attributes should be listed
      | username | email          | is_staff    | is_admin |
      | user0    | user0@test.com | False       | False    |
      | user1    | user1@test.com | #uu1?test12 | False    |
