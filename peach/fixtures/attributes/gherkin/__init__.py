from behave.model import Feature, Scenario

from ...fixtures import Fixture


class Gherkin(Fixture):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_feature_tags(cls) -> list[str]:
        feature: Feature = cls()._ctx.feature  # pyright: ignore
        return feature.tags

    @classmethod
    def get_scenario_tags(cls) -> list[str]:
        scenario: Scenario = cls()._ctx.scenario
        return scenario.tags
