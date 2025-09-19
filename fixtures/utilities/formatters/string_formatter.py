import textwrap


def to_sentence_case(s: str):
    try:
        return s.capitalize().replace("_", " ")
    except Exception:
        return s


def indent(s: str, indent=2):
    try:
        return textwrap.indent(s, " " * indent)
    except Exception:
        return s
