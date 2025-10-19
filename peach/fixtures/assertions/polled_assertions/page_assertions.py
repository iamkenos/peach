from peach.plugins.page.types import Page

from ..base_assertions import Any, Assertion
from . import PolledAssertions


class PageAssertions(PolledAssertions):
    def __init__(self, page: Page, **kwargs):
        super().__init__(timeout=page.timeout, **kwargs)
        self.__page = page

    def dom_content_loaded(self, *, is_not=False, **kwargs: Any):
        def success_criteria(this: Assertion):
            try:
                self.__page.wait_for_load_state(this.expected)
            except Exception:
                this.set_actual(False)
            this.set_actual(this.expected)
            return this.expected == this.actual

        assertion = Assertion(self.dom_content_loaded, is_not=is_not, **kwargs)
        assertion.set_expected("domcontentloaded")
        assertion.set_success_criteria(success_criteria)
        return self.add_assertion(assertion)

    def url_contains(self, expected: Any, *, is_not=False, **kwargs: Any):
        def success_criteria(this: Assertion):
            this.set_actual(self.__page.url)
            return this.args.substring in this.actual

        assertion = Assertion(self.url_contains, is_not=is_not, **kwargs)
        assertion.set_expected("Url contains substring")
        assertion.set_success_criteria(success_criteria)
        assertion.args.substring = expected
        return self.add_assertion(assertion)

    def url_equals(self, expected: Any, *, is_not=False, **kwargs: Any):
        def success_criteria(this: Assertion):
            this.set_actual(self.__page.url)
            return this.expected == this.actual

        assertion = Assertion(self.url_equals, is_not=is_not, **kwargs)
        assertion.set_expected(expected)
        assertion.set_success_criteria(success_criteria)
        return self.add_assertion(assertion)
