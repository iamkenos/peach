"""Typehub to avoid circular imports for other modules under context."""

from typing import TYPE_CHECKING, Any


class Attr:
    _ctx = "_ctx"
    ctx = "ctx"


if TYPE_CHECKING:
    from peach.plugins.context import Context as _Context

if TYPE_CHECKING:
    Context = _Context
else:
    Context = Any
