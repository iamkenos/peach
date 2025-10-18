import textwrap

import slugify
import textcase
from behave._types import parse_bool


class Colors:
    RED = "\033[91m"
    RESET = "\033[0m"


def to_camel(s: str):
    try:
        return textcase.camel(s)
    except Exception:
        return s


def to_constant(s: str):
    try:
        return textcase.constant(s)
    except Exception:
        return s


def to_kebab(s: str):
    try:
        return textcase.kebab(s)
    except Exception:
        return s


def to_lower(s: str):
    try:
        return textcase.lower(s)
    except Exception:
        return s


def to_pascal(s: str):
    try:
        return textcase.pascal(s)
    except Exception:
        return s


def to_sentence(s: str):
    try:
        return textcase.sentence(s)
    except Exception:
        return s


def to_slug(s: str, **kwargs):
    try:
        return slugify.slugify(s, **kwargs)
    except Exception:
        return s


def to_snake(s: str):
    try:
        return textcase.snake(s)
    except Exception:
        return s


def to_title(s: str):
    try:
        return textcase.upper(s)
    except Exception:
        return s


def to_upper(s: str):
    try:
        return textcase.upper(s)
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
