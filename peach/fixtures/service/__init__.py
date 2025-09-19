from peach.fixtures.assertions.polled_assertions import PolledAssertions

from ...fixtures import Fixture


class WebService(Fixture):
    def __init__(self):
        super().__init__()
        self.timeout = self._ctx.env.api_request_timeout

    def expect(self, **kwargs) -> PolledAssertions:
        return PolledAssertions(self.timeout, **kwargs)
