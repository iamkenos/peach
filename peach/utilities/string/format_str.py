# pyright: reportWildcardImportFromLibrary=false
import textwrap

from behave._types import parse_bool
from inflection import *  # noqa: F403


class Colors:
    RED = "\033[91m"
    RESET = "\033[0m"


def to_sentence_case(s: str):
    try:
        return s.capitalize().replace("_", " ")
    except Exception:
        return s


def to_maybe_bool(s: str):
    try:
        return parse_bool(s)
    except Exception:
        return s


def indent(s: str, indent=2):
    try:
        return textwrap.indent(s, " " * indent)
    except Exception:
        return s


def ansi_red(s: str):
    try:
        return f"{Colors.RED}{s}{Colors.RESET}"
    except Exception:
        return s
