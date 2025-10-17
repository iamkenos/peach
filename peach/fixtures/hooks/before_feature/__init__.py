from behave.model import Feature, Scenario, ScenarioOutline

from .. import Hook


class BeforeFeature(Hook):
    def __init__(self, feature: Feature):
        super().__init__()
        self.feature = feature

    def __prefix_scenarios_with_idx(self) -> None:
        def do_prefix(idx: int, scenario: Scenario):
            scenario.name = f"S{idx + 1:02d}│{scenario.name}"

        for idx, s in enumerate(self.feature.scenarios):
            if isinstance(s, ScenarioOutline):
                for scenario in s.scenarios:
                    do_prefix(idx, scenario)
            elif isinstance(s, Scenario):
                do_prefix(idx, s)
            else:
                pass  # do nothing, unsupported type

    def run(self):
        self.__prefix_scenarios_with_idx()
