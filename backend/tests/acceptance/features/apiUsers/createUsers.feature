Feature: add user
  As an admin
  I want to be able to add users
  So that I can run my organization

  Scenario: admin creates a user
    Given user "brand-new-user" has been deleted
    When the administrator sends a detail of user with id "1" using restAPI GET request
    Then the HTTP status code should be "200"
    And response should contain following information
      | id           | 1     |
      | username     | admin |
      | is_superuser | true  |
      | is_staff     | true  |
