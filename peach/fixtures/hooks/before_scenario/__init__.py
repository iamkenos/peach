from behave.model import Scenario

from peach.utilities.object import inspect_obj

from .. import Hook


class BeforeScenario(Hook):
    def __init__(self, scenario: Scenario):
        super().__init__()
        self.scenario = scenario

    def __set_identifier_hash(self) -> None:
        if not self._ctx.is_using_behavex:
            inspect_obj.maybe_set_attribute(self.scenario, "identifier_hash", self._ctx.files.generate_uuid())

    def __suffix_name_with_example_id(self) -> None:
        """Suffixes the scenario name with the value of the first column of the example table."""
        if self.scenario._row is not None:
            id, *_ = list(self.scenario._row)
            self.scenario.name = f"{self.scenario.name}: {id}"

    def run(self):
        self.__set_identifier_hash()
        self.__suffix_name_with_example_id()
