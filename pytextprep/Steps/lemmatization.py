from ..registry import register_step
from ..validation import requires_str

def _lemmatize_word(word: str) -> str:

    """ Returns the lemma of one lowercase word """

    Irregular = {
        "children": "child", "mice": "mouse", "men": "man", "women": "woman",
        "feet": "foot", "teeth": "tooth", "geese": "goose", "people": "person",
        "went": "go", "gone": "go", "goes": "go",
        "was": "be", "were": "be", "been": "be", "is": "be", "are": "be", "am": "be",
        "has": "have", "had": "have", "does": "do", "did": "do", "done": "do",
        "ate": "eat", "saw": "see", "took": "take", "wrote": "write",
        "ran": "run", "came": "come", "made": "make", "said": "say",
    }

    if word in Irregular:
        return Irregular[word]

    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"

    stem = word[:-2]
    if word.endswith("es") and (stem.endswith("s") or stem.endswith("x") or stem.endswith("z") or stem.endswith("ch") or stem.endswith("sh")):
        return stem

    if word.endswith("s") and not (word.endswith("ss") or word.endswith("us") or word.endswith("is")) and len(word) > 2:
        return word[:-1]

    return word


@register_step("lemmatize")
@requires_str
def lemmatize(text: str) -> str:

    """ Rule-based lemmatizer: irregular forms first, then plural rules """

    Punct = ".,!?;:\"()[]{}"

    result = []
    for word in text.split():
        core = word.strip(Punct)
        lemma = _lemmatize_word(core.lower())

        if lemma:
            if core[0].isupper():
                lemma = lemma[0].upper() + lemma[1:]

            word = word.replace(core, lemma)

        result.append(word)

    return " ".join(result)