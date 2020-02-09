Feature: Step Parameters (tutorial03)

  Scenario: Blenders (simple-test with vars)
    Given I put "apples" in a blender
    When  I switch the blender on
    Then  it should transform into "apple juice"

  Scenario Outline: Use Blender with <thing> (scenario-outline)
    Given I put "<thing>" in a blender
    When I switch the blender on
    Then it should transform into "<other thing>"

    Examples: Amphibians
      | thing         | other thing |
      | Red Tree Frog | mush        |
      | apples        | apple juice |

    Examples: Consumer Electronics
      | thing        | other thing |
      | iPhone       | toxic waste |
      | Galaxy Nexus | toxic waste |

  Scenario: Some scenario with inline text
    Given a sample text loaded into the frobulator
        """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
    When we activate the frobulator
    Then we will find it similar to English

  Scenario: Setup Table
    Given a set of specific users
      | name      | department  |
      | Barry     | Beer Cans   |
      | Pudey     | Silly Walks |
      | Two-Lumps | Silly Walks |
    When we count the number of people in each department
    Then we will find two people in "Silly Walks"
    But we will find one person in "Beer Cans"

  Scenario: Unordered Result Table Comparison (RowFixture Table)
    Given a set of specific users
      | name   | department  |
      | Alice  | Beer Cans   |
      | Bob    | Beer Cans   |
      | Charly | Silly Walks |
      | Dodo   | Silly Walks |
    Then we will have the following people in "Silly Walks"
      | name   |
      | Charly |
      | Dodo   |
    And we will have the following people in "Beer Cans"
      | name  |
      | Bob   |
      | Alice |

  Scenario: Subset Result Table Comparison
    Given a set of specific users
      | name  | department       |
      | Alice | Super-sonic Cars |
      | Bob   | Super-sonic Cars |
    Then we will have at least the following people in "Super-sonic Cars"
      | name  |
      | Alice |
