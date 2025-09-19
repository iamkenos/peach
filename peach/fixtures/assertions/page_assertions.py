# pyright: reportIncompatibleVariableOverride=false


from peach.plugins.page.types import Page

from .polled_assertions import Any, PolledAssertion, PolledAssertions


class PageAssertions(PolledAssertions):
    def __init__(self, page: Page, **kwargs):
        super().__init__(page.timeout, **kwargs)
        self.page = page

    def dom_content_loaded(self, **kwargs: Any):
        assertion = PolledAssertion(self.dom_content_loaded.__name__, **kwargs)
        assertion.expected = "domcontentloaded"
        assertion.actual_predicate = lambda: self.page.wait_for_load_state(assertion.expected)
        assertion.is_success = lambda: True
        return self.add_assertion(assertion)

    def url_contains(self, substring: Any, **kwargs: Any):
        assertion = PolledAssertion(self.url_contains.__name__, **kwargs)
        assertion.expected = "Url contains substring"
        assertion.actual_predicate = lambda: self.page.url
        assertion.is_success = lambda: substring in assertion.actual
        assertion.args.substring = substring
        return self.add_assertion(assertion)

    def url_equals(self, expected: Any, **kwargs: Any):
        assertion = PolledAssertion(self.url_equals.__name__, **kwargs)
        assertion.expected = expected
        assertion.actual_predicate = lambda: self.page.url
        assertion.is_success = lambda: assertion.actual == assertion.expected
        return self.add_assertion(assertion)
