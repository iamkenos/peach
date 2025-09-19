Feature: Feature One

  Background:
    Given I have something
  @run
  Scenario Outline: Foo
    When I say foo
      And I say bar
    Then I expect something

    Examples:
      | data_id | value |
      | 1       | A     |
      | 2       | B     |
