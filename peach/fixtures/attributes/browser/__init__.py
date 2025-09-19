import os
import uuid

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import BrowserContext, Playwright

from peach.fixtures import Fixture
from peach.fixtures.attributes.env import DEFAULT_TIMEOUT
from peach.plugins.page.types import Page


class Browser(Fixture):
    def __init__(self):
        super().__init__()
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
        proxy, headless, timeout = self._ctx.env.browser_proxy, self._ctx.env.browser_is_headless, self._ctx.env.browser_timeout
        context = self.launcher.chromium.launch(headless=headless).new_context(ignore_https_errors=True, proxy=proxy)
        context.set_default_timeout(timeout * 1000)
        context.set_default_navigation_timeout(max(timeout, DEFAULT_TIMEOUT) * 1000)  # navigation timeout shouldn't be less than the default
        return context

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
            full_path = self._ctx.attach_evidence(filename, lambda full_path: self.page.screenshot(path=full_path, full_page=True))

            try:
                # doesnt work with the default behavex html formatter anymore, library issue?
                self._ctx.bhximgs_attached_images_folder = os.path.dirname(self._ctx.evidence_path)
                image_attachments.attach_image_file(self._ctx, full_path, filename)
            except Exception:
                pass
