import uuid

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import BrowserContext, Playwright

from peach.fixtures import Fixture
from peach.fixtures.attributes.env import DEFAULT_TIMEOUT
from peach.plugins.page.types import Page
from peach.utilities.formatters.datetime_formatter import seconds_to_ms


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
        proxy = self._ctx.env.browser_proxy
        headless = self._ctx.env.browser_is_headless
        timeout = self._ctx.env.browser_timeout

        # fmt: off
        context = self.launcher.chromium \
            .launch(headless=headless, args=["--start-maximized"]) \
            .new_context(
                ignore_https_errors=True,
                proxy=proxy,
                record_video_dir=self._ctx.evidence_path,
                no_viewport=True)
        # fmt: on
        # navigation timeout shouldn't be less than the default
        context.set_default_navigation_timeout(seconds_to_ms(max(timeout, DEFAULT_TIMEOUT)))
        context.set_default_timeout(seconds_to_ms(timeout))
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
                self._ctx.bhximgs_attached_images_folder = self._ctx.scenario_log_dir()
                image_attachments.attach_image_file(self._ctx, full_path, filename)
            except Exception:
                pass
