from ..registry import register_step
from ..validation import requires_str
import unicodedata

@register_step("remove_accents")
@requires_str
def remove_accents(text: str) -> str:
    # NFKD: decomposes composed characters (é -> e + ´) and converts special forms to plain ones ① -> 1
    d = unicodedata.normalize("NFKD", text)
    result = []
    for c in d:
        # unicodedata.combining(i): returns a value > 0 if c is a combining mark (accent), so we drop it.
        if unicodedata.combining(c):
            continue
        result.append(c)
    return "".join(result)