Feature: add user
  As an admin
  I want to be able to add users
  So that I can run my organization

  Scenario: admin creates a user
    Given user "brand-new-user" has been deleted
    When the administrator sends a user creation request for user "brand-new-user" password "$%gt67AS52" using POST request
    And the HTTP status code should be "200"
    And user "brand-new-user" should exist

