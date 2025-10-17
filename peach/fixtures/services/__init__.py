from urllib.parse import urljoin

import requests

from ...fixtures import Fixture


class RequestClient(Fixture):
    def __init__(self, base_url: str):
        super().__init__()
        self.__base_url = base_url
        self.__verify = self._ctx.env.api_request_verify_tls
        self.__timeout = self._ctx.env.api_request_timeout

    def __request(self, method: str, url: str, **kwargs):
        url = str(urljoin(self.__base_url, kwargs.get(url, "")))
        kwargs.setdefault("verify", self.__verify)
        kwargs.setdefault("timeout", self.__timeout)

        return requests.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.__request(self.get.__name__, url, **kwargs)

    def post(self, url, **kwargs):
        return self.__request(self.post.__name__, url, **kwargs)

    def put(self, url, **kwargs):
        return self.__request(self.put.__name__, url, **kwargs)

    def patch(self, url, **kwargs):
        return self.__request(self.patch.__name__, url, **kwargs)

    def delete(self, url, **kwargs):
        return self.__request(self.delete.__name__, url, **kwargs)


class RequestHeaders(Fixture):
    def __init__(self):
        super().__init__()
        self.url = ""

    def content_type(self, value: str):
        return {"Content-Type": f"{value}"}

    def content_type_app_json(self):
        return self.content_type("application/json")


class Endpoints(Fixture):
    def __init__(self):
        super().__init__()


class WebService(Fixture):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.version = ""
        self.headers = RequestHeaders()
        self.endpoints = Endpoints()

    @property
    def request(self):
        return RequestClient(self.url)
