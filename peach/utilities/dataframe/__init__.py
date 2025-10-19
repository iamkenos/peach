import pendulum  # noqa

import inspect

from dataclasses import dataclass
from pandas import DataFrame, Series
from typing import Callable, List, Any, Optional

from peach.fixtures.assertions import Assertions


@dataclass
class Filter:
    name: str
    condition: Callable[[DataFrame], DataFrame]
    description: Optional[str] = None

    def __post_init__(self):
        self.name = f"filter.{self.name}(...)"
        if self.description is None:
            self.description = inspect.getsource(self.condition).strip().rstrip(",").lstrip("condition=")


class DataFrameFilter:
    """
    Interface for lazy-filtering a dataframe.
    """

    def __init__(self, df: DataFrame):
        self.__source_df = df
        self.__filters: List[Filter] = []

    def reset(self):
        self.__filters.clear()
        return self

    def by_id(self, id: Any):
        filter = Filter(
            name=self.by_id.__name__,
            condition=lambda df: df[df.id == id],
            description=f"id == {id}",
        )
        self.__filters.append(filter)
        return self

    def by_column(self, column: str, value: Any):
        filter = Filter(
            name=self.by_column.__name__,
            condition=lambda df: df[df[column] == value],
            description=f"{column} == {value}",
        )
        self.__filters.append(filter)
        return self

    def describe(self):
        filepath = getattr(self.__source_df, "source_file", None)
        header = f"Filepath: {filepath}\n" if filepath else ""
        if not self.__filters:
            return f"{header}\n"

        return f"{header}Filters:" + "".join(map(lambda f: f"\n  - {f.name}: {f.description}", self.__filters)) + "\n"

    def apply(self):
        expect = Assertions()
        failed_filters = []

        df = self.__source_df.copy(deep=True)
        for f in self.__filters:
            try:
                df = f.condition(df)
            except Exception as e:
                failed_filter = f"{f.name} -> {str(e)}"
                failed_filters.append(failed_filter)

        expect.set_exception_type().predicate(
            lambda: len(failed_filters) == 0,
            failed_filters=failed_filters,
            message=f"Unable to apply {'all' if len(failed_filters) == len(self.__filters) else 'some'} of the filters.",
        ).evaluate()

        return df

    def nth(self, row: int) -> Series:
        """Use 1-based indexing."""
        expect = Assertions()
        df = self.apply()

        expect.set_exception_type(IndexError).predicate(
            lambda: row >= 1 and len(df) >= row,
            total_rows=len(df),
            message=f"Unable to get row {row} from the dataframe.",
        ).evaluate()

        o_based_index = row - 1
        return df.iloc[o_based_index]

    def first(self) -> Series:
        return self.nth(1)
