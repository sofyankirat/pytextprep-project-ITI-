from ..registry import register_step
from ..validation import requires_str
import re

@register_step("normalize_arabic")
@requires_str
def normalize_arabic(text: str, taa_marbuta: bool = False) -> str:

    Remove = re.compile("[\u064B-\u0652\u0670\u0640]")
    Map = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي"})
    text = Remove.sub("", text)
    text = text.translate(Map)
    if taa_marbuta:
        text = text.replace("ة", "ه")
    return text