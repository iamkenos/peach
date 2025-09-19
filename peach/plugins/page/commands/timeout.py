from peach.plugins.page.types import Page


@property
def timeout(self: Page) -> int:
    return self._ctx.env.browser_timeout
