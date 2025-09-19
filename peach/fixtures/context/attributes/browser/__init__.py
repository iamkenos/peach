import uuid

from playwright._impl._browser_context import BrowserContext
from playwright._impl._page import Page
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Playwright

from peach.fixtures.context.types import Context


class Browser:
    def __init__(self, ctx: Context):
        self._ctx = ctx
        self.launcher: Playwright = None
        self.page: Page = None

    def start(self) -> None:
        self.launcher = sync_playwright().start()

    def stop(self) -> None:
        if self.page and self.page.context:
            self.page.context.close()
        if self.launcher:
            self.launcher.stop()

    def create(self) -> BrowserContext:
        proxy, headless = self._ctx.env.browser_proxy, self._ctx.env.browser_is_headless
        self.launcher.chromium.launch(headless=headless).new_context(ignore_https_errors=True, proxy=proxy)
        return self.launcher.chromium.launch(headless=headless).new_context(ignore_https_errors=True, proxy=proxy)

    def navigate(self, url: str):
        """Creates a new page from a fresh browser context and navigates to the given url."""
        self.page = self.create().new_page()
        self.page.goto(url)

    def attach_screenshot(self, name=None) -> None:
        try:
            from behavex_images import image_attachments
        except ImportError:
            image_attachments = None

        if self.page and image_attachments:
            filename = f"{name or uuid.uuid4().hex}.png"

            def callback(_, full_path):
                return self.page.screenshot(path=full_path, full_page=True)

            self._ctx.attach_evidence(filename, callback)
            # image_attachments.attach_image_file(self.ctx, full_path, name)  # doesnt work, library issue?
