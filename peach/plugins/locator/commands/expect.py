from peach.fixtures.assertions.polled_assertions.locator_assertions import LocatorAssertions
from peach.plugins.locator.types import Locator


def expect(self: Locator, **kwargs) -> LocatorAssertions:
    return LocatorAssertions(self, **kwargs)
