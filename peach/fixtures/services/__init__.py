from typing import Any
from urllib.parse import urljoin, urlsplit

import requests
from requests import Response

from peach.fixtures.assertions.polled_assertions.api_assertions import ApiAssertions
from peach.utilities.object import format_obj
from peach.utilities.string import format_str

from ...fixtures import Fixture
from .types import RequestClient


class RequestSpec(Fixture):
    def __init__(self, client: RequestClient, *, method: str, path: str, **kwargs):
        super().__init__()
        self.__client = client
        self.__method = method
        self.__path = path
        self.__kwargs = kwargs

    def expect(self, **kwargs):
        return ApiAssertions(self, **kwargs)

    def send(self):
        url = str(urljoin(self.__client.base_url, self.__path))
        self.__kwargs.setdefault("verify", self.__client.verify)
        self.__kwargs.setdefault("timeout", self.__client.timeout)

        req: Any = dict(method=self.__method, url=url, **self.__kwargs)
        response: Response = requests.request(**req)

        if self.__client.attachments_enabled:
            attachment_prefix = format_str.to_slug(urlsplit(url).path)

            def get_response_content(response: Response):
                try:
                    return response.json()
                except Exception:
                    return response.text

            request_attachment = dict(**req)
            response_attachment = dict(status=response.status_code, content=get_response_content(response))
            self._ctx.files.output.try_create_evidence_file(f"{attachment_prefix}-request.json", str(format_obj.beautify(request_attachment)))
            self._ctx.files.output.try_create_evidence_file(f"{attachment_prefix}-response.json", str(format_obj.beautify(response_attachment)))

        return response


class RequestClient(Fixture):
    def __init__(
        self,
        *,
        base_url: str,
        attachments_enabled: bool = False,
    ):
        super().__init__()
        self.__base_url = base_url
        self.__verify = self._ctx.env.api_request_verify_tls
        self.__timeout = self._ctx.env.api_request_timeout
        self.__attachments_enabled: bool = attachments_enabled

    @property
    def base_url(self):
        return self.__base_url

    @property
    def verify(self):
        return self.__verify

    @property
    def timeout(self):
        return self.__timeout

    @property
    def attachments_enabled(self):
        return self.__attachments_enabled

    def get(self, path, **kwargs):
        return RequestSpec(self, method=self.get.__name__, path=path, **kwargs)

    def post(self, path, **kwargs):
        return RequestSpec(self, method=self.post.__name__, path=path, **kwargs)

    def put(self, path, **kwargs):
        return RequestSpec(self, method=self.put.__name__, path=path, **kwargs)

    def patch(self, path, **kwargs):
        return RequestSpec(self, method=self.patch.__name__, path=path, **kwargs)

    def delete(self, path, **kwargs):
        return RequestSpec(self, method=self.delete.__name__, path=path, **kwargs)


class RequestHeaders(Fixture):
    def __init__(self):
        super().__init__()

    def content_type(self, value: str):
        return {"Content-Type": f"{value}"}

    def content_type_app_json(self):
        return self.content_type("application/json")

    def content_type_app_x_form_url_encoded(self):
        return self.content_type("application/x-www-form-urlencoded")

    def content_type_txt_string(self):
        return self.content_type("text/plain")


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
        self.__attachments_enabled: bool = True

    def attach(self, state=True):
        """Switch to include the request and response payloads in the report attachments.

        Args:
            state (bool, optional): The switch state. Defaults to True.
        """
        self.__attachments_enabled = state
        return self

    @property
    def request(self):
        return RequestClient(base_url=self.url, attachments_enabled=self.__attachments_enabled)
