import re
from importlib import resources
from ..registry import register_step
from ..validation import requires_str

@register_step("word_tokenize")
@requires_str
def word_tokenize(text: str) -> list:

    """
        Input: A string
        Process: Splits into words; keeps internal apostrophes and hyphens; drops punctuation
        Output: List with the matched words
    """

    Word_Token = re.compile(r"[^\W_]+(?:['-][^\W_]+)*")
    return Word_Token.findall(text)

@register_step("sent_tokenize")
@requires_str
def sent_tokenize(text: str) -> list:

    """
        Input: A string
        Process: Splits after ., ! or ? followed by a space and a capital letter or digit; does not split after common abbreviations (Dr., Mr., Mrs., e.g., i.e., etc.) or inside numbers like 3.14
        Output: List with the matched sentences
    """

    Sent_Token = re.compile(r"[.!?]+(?=\s+[A-Z0-9])")

    sentences = []
    start = 0
    
    Abbreviations = {"dr.", "mr.", "mrs.", "e.g.", "i.e.", "etc."} # set to speed the searching

    for i in Sent_Token.finditer(text):
        end = i.end()
        chunk = text[start:end]
        # lstrip removes any leading characters found in the given set
        # stopping at the first character that isn't in the set
        # solves this test case for instance 'He said "Dr. Ali" came. Then he left'
        last = (chunk.split())[-1].lstrip('"\'([{') 
        if last.lower() in Abbreviations:
            continue

        sentences.append(text[start:end].strip())
        start = end

    rest = text[start:].strip()
    if rest:
        sentences.append(rest)

    return sentences

def _load_stopwords():

    """ Load the stopwords from stopwords_en.txt as a set """

    path = resources.files("pytextprep").joinpath("resources", "stopwords_en.txt")
    text = path.read_text(encoding="utf-8")
    
    words = set()
    for w in text.splitlines():
        w = w.strip()
        if w:
            words.add(w.lower())

    return words

@register_step("remove_stopwords")
@requires_str
def remove_stopwords(text: str, custom_words: list=None, extra_only: bool=False) -> str:

    """
        Input: A string and the list of the custom words if it exists and a boolean value that determines what is the lists that we will work on
        Process: Case-insensitive. Uses the built-in English list plus custom_words; extra_only=True uses only the custom list. Keeps negations (not, no, nor) because they flip meaning
        Output: A string without the stopwords
    """

    message = text.split()
    ans = []
    words = set()
    if extra_only == False:
        words = _load_stopwords()
    if custom_words and extra_only == False:
        custom_words = {w.lower() for w in custom_words}
        words = words | set(custom_words)
    elif custom_words and extra_only == True:
        custom_words = {w.lower() for w in custom_words}
        words = set(custom_words)
    for i in message:
        if i.lower() not in words:
            ans.append(i)

    return " ".join(ans)

def _load_contractions():

    """ Load the contractions from contractions_en.tsv as a dictionary """
    path = resources.files("pytextprep").joinpath("resources", "contractions_en.tsv")
    text = path.read_text(encoding="utf-8")

    table = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        key, value = line.split(None, 1) # split on any whitespace (space or tabs) once
        table[key.strip().lower()] = value.strip()
    return table


@register_step("expand_contractions")
@requires_str
def expand_contractions(text: str) -> str:

    """
        Input: A string
        Process: Table-driven; handles ' and the curly ’; keeps the capital of the first letter
        Output: A string with contractions expanded
    """

    Punct = ".,!?;:\"()[]{}"
    message = text.replace("’", "'")
    table = _load_contractions()
    result = []

    for word in message.split():
        core = word.strip(Punct)
        key = core.lower()

        if key in table:
            extend = table[key]
            if core[0].isupper():
                extend = extend[0].upper() + extend[1:]
            word = word.replace(core, extend)

        result.append(word)

    return " ".join(result)