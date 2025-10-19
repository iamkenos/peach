import json
from typing import Any

import numpy as np

from ..string import format_str


def beautify(json_like: Any, indent=2):
    try:
        if isinstance(json_like, (list, dict)):
            return json.dumps(json_like, indent=indent)
        return json_like
    except Exception:
        return json_like


def humanize(o: Any, sep=":"):
    args: list = []
    for key, value in o.items():
        prop = format_str.to_sentence(key)
        value = format_str.indent(f"\n{beautify(value)}") if isinstance(value, (list, dict)) else value
        args.append(f"\n{prop}{sep} {value}")
    result = "".join(args).strip() if args else ""
    return result


def remove_nullish(json_like: Any, considered_nullish=[]):
    try:
        nullish_values = [None, np.nan, *considered_nullish]
        if isinstance(json_like, dict):
            return {k: v for k, v in json_like.items() if v not in nullish_values}
        elif isinstance(json_like, list):
            return [i for i in json_like if i not in nullish_values]
        else:
            raise TypeError()
    except Exception:
        return json_like
