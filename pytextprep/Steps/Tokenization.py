import re
from ..Steps import register_step
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

    
