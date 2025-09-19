"""Typehub to avoid circular imports for other modules under page."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from page import Page as _Page

if TYPE_CHECKING:
    Page = _Page
else:
    Page = Any
