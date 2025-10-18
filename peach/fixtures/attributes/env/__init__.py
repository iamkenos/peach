import os
from typing import Any, Dict

from dotenv import load_dotenv
from filelock import FileLock
from playwright._impl._api_structures import ProxySettings

from peach.fixtures import Fixture
from peach.utilities.object import inspect_obj
from peach.utilities.string import format_str

DEFAULT = "UNDEFINED"
DEFAULT_TIMEOUT = 30


class Env(Fixture):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.register()

    def register(self):
        self.__set_sys_vars()
        self.__set_api_vars()
        self.__set_browser_vars()

    def __set_sys_vars(self):
        http_proxy, https_proxy, no_proxy = "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"
        env_http_proxy = os.getenv(http_proxy, os.getenv(http_proxy.lower(), None)) or None
        env_https_proxy = os.getenv(https_proxy, os.getenv(https_proxy.lower(), None)) or None
        env_no_proxy = os.getenv(no_proxy, os.getenv(no_proxy.lower(), None)) or None

        self.http_proxy = env_http_proxy
        self.https_proxy = env_https_proxy
        self.no_proxy = env_no_proxy

    def __set_api_vars(self):
        self.api_request_verify_tls = format_str.to_maybe_bool(os.getenv("REQUEST_VERIFY_TLS", str(True)))
        try:
            self.api_request_timeout = int(eval(str(os.getenv("REQUEST_TIMEOUT", DEFAULT_TIMEOUT))))
        except Exception:
            self.api_request_timeout = DEFAULT_TIMEOUT

    def __set_browser_vars(self):
        proxy, bypass = self.http_proxy or self.https_proxy, self.no_proxy
        self.browser_proxy: ProxySettings = dict(server=proxy, bypass=bypass) if bool(proxy) else None
        self.browser_is_headless = os.getenv("BROWSER_IS_HEADLESS", DEFAULT).lower() != "false"
        try:
            self.browser_timeout = int(eval(str(os.getenv("BROWSER_TIMEOUT", DEFAULT_TIMEOUT))))
        except Exception:
            self.browser_timeout = DEFAULT_TIMEOUT

    def get_resolved_as_dict(self) -> Dict[str, Any]:
        attrs = inspect_obj.get_own_attributes(self)

        kvps = {}
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value is not DEFAULT and bool(value):  # only return those that are defined
                kvps[attr.upper()] = value
        return kvps

    def export_resolved_as_file(self, filepath: str, should_mask_sensitive=True):
        lock_file = filepath + ".lock"

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        lock = FileLock(lock_file, timeout=0)

        try:
            with lock:
                if not os.path.exists(filepath):
                    with open(filepath, "w") as f:
                        for key, value in self.get_resolved_as_dict().items():
                            if should_mask_sensitive:
                                sensitive_keywords = ["key", "token", "secret", "password", "passphrase"]
                                is_key_sensitive = any(word in f"_{key.lower()}" for word in sensitive_keywords)
                                if is_key_sensitive:
                                    value = "*" * 8
                            if isinstance(value, bool):
                                value = str(value).lower()
                            f.write(f"{key}={value}\n")

        except TimeoutError:
            pass
