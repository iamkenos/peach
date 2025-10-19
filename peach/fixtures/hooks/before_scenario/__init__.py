from typing import Any

from behave.model import Scenario

from peach.utilities.object import inspect_obj
from peach.utilities.string import format_str

from .. import Hook


class BeforeScenario(Hook):
    def __init__(self, scenario: Scenario):
        super().__init__()
        self.scenario = scenario

    def __set_identifier_hash(self) -> None:
        if not self._ctx.is_using_behavex:
            inspect_obj.maybe_set_attribute(self.scenario, "identifier_hash", self._ctx.files.generate_uuid())

    def __transform_row_headings(self) -> None:
        """Mutates row headings to snake_case."""
        if self.scenario._row is not None:
            row: Any = self.scenario._row
            transformed_headings = list(map(lambda h: format_str.to_snake(h), row.headings))

            self.scenario._row.headings = transformed_headings

    def __suffix_name_with_example_id(self) -> None:
        """Suffixes the scenario name with the value of the first column of the example table."""
        if self.scenario._row is not None:
            id, *_ = list(self.scenario._row)
            self.scenario.name = f"{self.scenario.name}: {id}"

    def run(self):
        self.__set_identifier_hash()
        self.__transform_row_headings()
        self.__suffix_name_with_example_id()
