from peach.plugins.locator.types import Locator

from ..base_assertions import Any, Assertion
from . import PolledAssertions


class LocatorAssertions(PolledAssertions):
    def __init__(self, locator: Locator, **kwargs):
        super().__init__(timeout=locator.page.timeout, **kwargs)
        self.__locator = locator

    def displayed(self, *, is_not=False, **kwargs: Any):
        def success_criteria(this: Assertion):
            this.set_actual(self.__locator.is_visible())
            this.args.locator = self.__locator._selector
            return this.expected == this.actual

        assertion = Assertion(self.displayed, is_not=is_not, **kwargs)
        assertion.set_expected(True)
        assertion.set_success_criteria(success_criteria)
        return self.add_assertion(assertion)
