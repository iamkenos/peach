import re

from peach.plugins.locator.types import Locator


@property
def _selector(self: Locator) -> str:
    source = str(self)
    rex_match = re.search(r"selector=(['\"])(.*?)\1", source)

    try:
        if rex_match:
            return rex_match.group(2)
        else:
            return source
    except Exception:
        return source
