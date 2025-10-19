"""Typehub to avoid circular imports for other modules under page."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from peach.fixtures.services import RequestClient as _RequestClient
    from peach.fixtures.services import RequestSpec as _RequestSpec
    from peach.fixtures.services import Response as _Response

if TYPE_CHECKING:
    RequestClient = _RequestClient
    RequestSpec = _RequestSpec
    Response = _Response
else:
    RequestClient = Any
    RequestSpec = Any
    Response = Any
