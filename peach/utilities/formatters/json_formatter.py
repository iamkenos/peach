import json


def beautify(json_like: list | dict, indent=2):
    try:
        if isinstance(json_like, (list, dict)):
            return json.dumps(json_like, indent=indent)
        return json_like
    except Exception:
        return json_like
