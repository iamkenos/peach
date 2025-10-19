# pyright: reportIncompatibleMethodOverride=false
import typing
from typing import Literal

from playwright.sync_api._generated import Locator as BaseLocator

from peach.fixtures.assertions.polled_assertions.locator_assertions import LocatorAssertions
from peach.plugins.page.types import Page


class Locator(BaseLocator):
    """
    The playwright `locator` extended with custom commands.

    This is mainly used for type completion.
    Unfortunately python can't infer the args and return types of overriden playwright methods, so we have to redeclare them here.
    """

    # ==================================
    #   custom commands
    # ==================================
    @property
    def _selector(self) -> str: ...

    def expect(self, **kwargs) -> LocatorAssertions: ...

    def wait_until(self, **kwargs) -> LocatorAssertions: ...

    # ==================================
    #   overrides
    # ==================================
    @property
    def page(self) -> "Page": ...

    @property
    def first(self) -> "Locator": ...

    @property
    def last(self) -> "Locator": ...

    def locator(
        self,
        selector_or_locator: typing.Union[str, "Locator"],
        *,
        has_text: typing.Optional[typing.Union[typing.Pattern[str], str]] = None,
        has_not_text: typing.Optional[typing.Union[typing.Pattern[str], str]] = None,
        has: typing.Optional["Locator"] = None,
        has_not: typing.Optional["Locator"] = None,
    ) -> "Locator": ...

    def get_by_alt_text(
        self,
        text: typing.Union[str, typing.Pattern[str]],
        *,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def get_by_label(
        self,
        text: typing.Union[str, typing.Pattern[str]],
        *,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def get_by_placeholder(
        self,
        text: typing.Union[str, typing.Pattern[str]],
        *,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def get_by_role(
        self,
        role: Literal[
            "alert",
            "alertdialog",
            "application",
            "article",
            "banner",
            "blockquote",
            "button",
            "caption",
            "cell",
            "checkbox",
            "code",
            "columnheader",
            "combobox",
            "complementary",
            "contentinfo",
            "definition",
            "deletion",
            "dialog",
            "directory",
            "document",
            "emphasis",
            "feed",
            "figure",
            "form",
            "generic",
            "grid",
            "gridcell",
            "group",
            "heading",
            "img",
            "insertion",
            "link",
            "list",
            "listbox",
            "listitem",
            "log",
            "main",
            "marquee",
            "math",
            "menu",
            "menubar",
            "menuitem",
            "menuitemcheckbox",
            "menuitemradio",
            "meter",
            "navigation",
            "none",
            "note",
            "option",
            "paragraph",
            "presentation",
            "progressbar",
            "radio",
            "radiogroup",
            "region",
            "row",
            "rowgroup",
            "rowheader",
            "scrollbar",
            "search",
            "searchbox",
            "separator",
            "slider",
            "spinbutton",
            "status",
            "strong",
            "subscript",
            "superscript",
            "switch",
            "tab",
            "table",
            "tablist",
            "tabpanel",
            "term",
            "textbox",
            "time",
            "timer",
            "toolbar",
            "tooltip",
            "tree",
            "treegrid",
            "treeitem",
        ],
        *,
        checked: typing.Optional[bool] = None,
        disabled: typing.Optional[bool] = None,
        expanded: typing.Optional[bool] = None,
        include_hidden: typing.Optional[bool] = None,
        level: typing.Optional[int] = None,
        name: typing.Optional[typing.Union[typing.Pattern[str], str]] = None,
        pressed: typing.Optional[bool] = None,
        selected: typing.Optional[bool] = None,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def get_by_test_id(  # noqa E501
        self, test_id: typing.Union[str, typing.Pattern[str]]
    ) -> "Locator": ...

    def get_by_text(
        self,
        text: typing.Union[str, typing.Pattern[str]],
        *,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def get_by_title(
        self,
        text: typing.Union[str, typing.Pattern[str]],
        *,
        exact: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def nth(self, index: int) -> "Locator": ...

    def describe(self, description: str) -> "Locator": ...

    def filter(
        self,
        *,
        has_text: typing.Optional[typing.Union[typing.Pattern[str], str]] = None,
        has_not_text: typing.Optional[typing.Union[typing.Pattern[str], str]] = None,
        has: typing.Optional["Locator"] = None,
        has_not: typing.Optional["Locator"] = None,
        visible: typing.Optional[bool] = None,
    ) -> "Locator": ...

    def or_(self, locator: "Locator") -> "Locator": ...

    def and_(self, locator: "Locator") -> "Locator": ...

    def all(self) -> typing.List["Locator"]: ...
