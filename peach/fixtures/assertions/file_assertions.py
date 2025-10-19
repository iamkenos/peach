import os
from typing import Any

from .base_assertions import Assertion, BaseAssertions


class FileAssertions(BaseAssertions):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def file_exists(self, filepath: str, *, is_not=False, **kwargs: Any):
        assertion = Assertion(self.file_exists, is_not=is_not, **kwargs)
        assertion.set_expected(True)
        assertion.set_actual(os.path.exists(filepath))
        assertion.set_success_criteria(lambda this: this.expected == this.actual)
        return self.add_assertion(assertion)
