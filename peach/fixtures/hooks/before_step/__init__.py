from typing import Any

from behave.model import Row, Step

from peach.utilities.string import format_str

from .. import Hook


class BeforeStep(Hook):
    def __init__(self, step: Step):
        super().__init__()
        self.step = step

    def __transform_table_headings(self) -> None:
        """Mutates table and rows to snake_case."""
        if self.step.table is not None:
            table: Any = self.step.table
            transformed_headings = list(map(lambda h: format_str.to_snake(h), table.headings))
            transformed_rows = list(map(lambda r: Row(headings=transformed_headings, cells=r.cells, line=r.line, comments=r.comments), table.rows))

            self.step.table.headings = transformed_headings
            self.step.table.rows = transformed_rows

    def run(self):
        self.__transform_table_headings()
