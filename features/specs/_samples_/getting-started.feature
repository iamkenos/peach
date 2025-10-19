Feature: Getting Started

  Background:
    Given a condition is met

  @init
  Scenario Outline: Run all examples
    When an event is triggered
    Then a condition is satisfied

    Examples:
      | data_id   | value |
      | TC-S1-001 | A     |
      | TC-S1-002 | B     |
      | TC-S1-003 | C     |
      | TC-S1-004 | D     |
      | TC-S1-005 | E     |

  Scenario Outline: Run selected examples
    When an event is triggered
    Then a condition is not satisfied
    And a condition is satisfied

    Examples:
      | data_id   | value |
      | TC-S1-001 | A     |
      | TC-S1-002 | B     |
      | TC-S1-003 | C     |

    @init @debug
    Examples:
      | data_id   | value |
      | TC-S1-004 | D     |

    Examples:
      | data_id   | value |
      | TC-S1-005 | E     |

  Scenario Outline: Run selected examples with pending steps
    When an event is not triggered
    Then a condition is satisfied

    Examples:
      | data_id   | value |
      | TC-S1-001 | A     |
      | TC-S1-002 | B     |
      | TC-S1-003 | C     |

    Examples:
      | data_id   | value |
      | TC-S1-004 | D     |

    @init
    Examples:
      | data_id   | value |
      | TC-S1-005 | E     |

  Scenario: Untagged scenario
    When an event is triggered
    Then a condition is satisfied

  @init
  Scenario: Tagged scenario
    When an event is triggered
    Then a condition is satisfied

  @init
  Scenario: Tagged scenario with pending steps
    When an event is not triggered
    Then a condition is satisfied

  @init
  Scenario: Scenarios using cucumber expressions and shared state across steps
    When a user does 1 action
    Then a total of 2 actions are performed

  Scenario Outline: Scenarios using custom parameter types and shared state across steps
    When an actor goes up
    Then the actor's last known position is <direction>

    @init
    Examples:
      | data_id   | direction |
      | TC-S1-001 | up        |
      | TC-S1-002 | down      |

  @init @poll
  Scenario: Poll a webservice response
    Then a different condition is not satisfied
