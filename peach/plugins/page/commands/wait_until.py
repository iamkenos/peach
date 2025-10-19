from peach.fixtures.assertions.polled_assertions.page_assertions import PageAssertions
from peach.plugins.page.types import Page


def wait_until(self: Page, **kwargs) -> PageAssertions:
    return PageAssertions(self, **kwargs).soft()
