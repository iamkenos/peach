from typing import Any
from urllib.parse import urljoin, urlsplit

import requests

from peach.utilities.datetime import pendulum
from peach.utilities.object import format_obj
from peach.utilities.string import format_str

from ...fixtures import Fixture


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
        self.__attachments_enabled = attachments_enabled
        self.__backoff_condition = None  # TODO: add backoff

    def __request(self, method: str, url: str, **kwargs):
        url = str(urljoin(self.__base_url, url))
        kwargs.setdefault("verify", self.__verify)
        kwargs.setdefault("timeout", self.__timeout)

        spec: Any = dict(method=method, url=url, **kwargs)
        res: requests.Response = requests.request(**spec)

        if self.__attachments_enabled:
            attach = self._ctx.files.output.try_create_evidence_file
            attachment_prefix = format_str.to_slug(urlsplit(url).path)
            attachment_suffix = pendulum.now().int_timestamp

            attach(f"{attachment_prefix}-request-{attachment_suffix}.json", str(format_obj.beautify(spec)))
            attach(f"{attachment_prefix}-response-{attachment_suffix}.json", str(format_obj.beautify(res.json())))

        return res

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
        self.__attachments_enabled = False

    def attach(self, state=True):
        """Switch to include the request and response payloads in the report attachments.

        Args:
            state (bool, optional): _description_. Defaults to True.
        """
        self.__attachments_enabled = state
        return self

    @property
    def request(self):
        return RequestClient(
            base_url=self.url,
            attachments_enabled=self.__attachments_enabled,
        )
