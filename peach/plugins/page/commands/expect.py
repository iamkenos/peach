from peach.fixtures.assertions.page_assertions import PageAssertions
from peach.plugins.page.types import Page


def expect(self: Page, **kwargs) -> PageAssertions:
    return PageAssertions(self, **kwargs)
