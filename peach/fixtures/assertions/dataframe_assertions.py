from typing import Any

from pandas import DataFrame

from .base_assertions import Assertion, BaseAssertions


class DataFrameAssertions(BaseAssertions):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def df_empty(self, actual: DataFrame, *, is_not=False, **kwargs: Any):
        assertion = Assertion(self.df_empty, is_not=is_not, **kwargs)
        assertion.set_expected("DataFrame is empty")
        assertion.set_actual(f"Found {len(actual.index)} records")
        assertion.set_success_criteria(lambda this: 0 == len(actual.index))
        return self.add_assertion(assertion)
