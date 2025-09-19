"""Typehub to avoid circular imports for other modules under locator."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from locator import Locator as _Locator

if TYPE_CHECKING:
    Locator = _Locator
else:
    Locator = Any
