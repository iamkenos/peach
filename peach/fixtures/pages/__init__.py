from peach.fixtures.assertions.polled_assertions.page_assertions import PageAssertions

from ...fixtures import Fixture


class WebComponent(Fixture):
    def __init__(self):
        super().__init__()
        self.browser = self._ctx.browser

    @property
    def page(self):
        return self._ctx.browser.page


class PageObject(WebComponent):
    def __init__(self):
        super().__init__()
        self.url = ""

    def navigate(self) -> None:
        self.browser.navigate(self.url)

    def expect(self, **kwargs) -> PageAssertions:
        return self.page.expect(**kwargs)

    def wait_until(self, **kwargs) -> PageAssertions:
        return self.page.wait_until(**kwargs)
