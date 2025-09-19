from peach.plugins.locator.types import Locator

from .polled_assertions import Any, PolledAssertion, PolledAssertions


class LocatorAssertions(PolledAssertions):
    def __init__(self, locator: Locator, **kwargs):
        super().__init__(locator.page.timeout, **kwargs)
        self.locator = locator

    def displayed(self, **kwargs: Any):
        assertion = PolledAssertion(self.displayed.__name__, **kwargs)
        assertion.expected = True
        assertion.actual_predicate = lambda: self.locator.is_visible()
        assertion.is_success = lambda: assertion.actual == assertion.expected
        assertion.args.locator = self.locator._selector
        return self.add_assertion(assertion)
