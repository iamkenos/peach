import os

from dotenv import load_dotenv

from fixtures.context.types import Context

DEFAULT = "UNDEFINED"


class Env:
    def __init__(self, ctx: Context):
        load_dotenv()
        self._ctx = ctx
        self.register()

    def register(self):
        self.__set_sys_vars()
        self.__set_browser_vars()

    def __set_sys_vars(self):
        http_proxy, https_proxy, no_proxy = "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"
        env_http_proxy = os.getenv(http_proxy, os.getenv(http_proxy.lower(), None)) or None
        env_https_proxy = os.getenv(https_proxy, os.getenv(https_proxy.lower(), None)) or None
        env_no_proxy = os.getenv(no_proxy, os.getenv(no_proxy.lower(), None)) or None

        self.http_proxy = env_http_proxy
        self.https_proxy = env_https_proxy
        self.no_proxy = env_no_proxy

    def __set_browser_vars(self):
        proxy, bypass = self.http_proxy or self.https_proxy, self.no_proxy
        self.browser_proxy = dict(server=proxy, bypass=bypass) if bool(proxy) else None
        self.browser_is_headless = os.getenv("BROWSER_IS_HEADLESS", DEFAULT).lower() != "false"
