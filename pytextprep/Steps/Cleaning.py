import re
import unicodedata
from itertools import groupby
import html

def lowercase(s: str) -> str:
    """
        Input: A string
        Process: transform the uppercase letters to the lowercase letters
        Output: A string with lowercase letters
    """

    if not isinstance(s, str):
        raise TypeError(f"expected str, got {type(s).__name__}")

    if len(s) == 0:
        return ""

    return s.casefold()


def normalize_whitespace(s: str) -> str:

    """
        Input: A string
        Process: Tabs, newlines and repeated spaces become one space; ends stripped
        Output: A string with tabs, newlines and repeated spaces replaced with a space
    """

    if not isinstance(s, str):
        raise TypeError(f"expected str, got {type(s).__name__}")

    if len(s) == 0:
        return ""

    temp = s.strip().split()
    temp2 = []
    for i in range(len(temp)):
        if temp[i].isspace():
            temp2.append(" ")
        else:
            temp2.append(temp[i])

    return(" ".join(temp2))

def remove_urls(text: str, replace_with: str="") -> str:
    """
        Input: A text and the characters that should replaced with the text
        Process: Replace the urls with the specified characters
        Output: Text after the replacement
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")

    if len(text) == 0:
        return ""

    s = ""
    ls = ['.', ',', '!', '?', ';', ':', ')']
    i = 0
    while i < len(text):
        if (i + 6 < len(text) and text[i] == 'h' and text[i + 1] == 't' and text[i + 2] == 't' and text[i + 3] == 'p' and text[
            i + 4] == ':' and text[i + 5] == '/' and text[i + 6] == '/') or (
                i + 7 < len(text) and text[i] == 'h' and text[i + 1] == 't' and text[i + 2] == 't' and text[i + 3] == 'p' and text[
            i + 4] == 's' and text[i + 5] == ':' and text[i + 6] == '/' and text[i + 7] == '/') or (
                i + 3 < len(text) and ((i - 1 != -1 and text[i - 1] == ' ') or i == 0) and text[i] == 'w' and text[i + 1] == 'w' and text[i + 2] == 'w' and text[i + 3] == '.'):
            while i < len(text) and text[i] != ' ':
                i += 1
            i -= 1
            while text[i] in ls:
                i -= 1
            s += replace_with
        else:
            s += text[i]
        i += 1
    return s

def remove_emails(text: str, replace_with: str="") -> str:
    """
        Input: A text and the characters that should replaced with the text
        Process: Replace the emails with the specified characters
        Output: Text after the replacement
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    
    if len(text) == 0:
        return ""

    Email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")

    return Email.sub(replace_with, text).strip()

def remove_punctuation(text: str, keep_emojis: bool=True) -> str:
    """
        Input: A text and a boolean value to know if the emojis will be kept
        Process: Apostrophes are deleted; every other punctuation or symbol character becomes a space. Emojis survive unless keep_emojis=False
        Output: Text after the replacement
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")

    if len(text) == 0:
        return ""
    
    text = text.replace("'", "")
    s = ""
    if keep_emojis == False:
        for i in range(len(text)):
            if not (text[i].isalnum() or text[i].isspace()):
                s += " "
            else:
                s += text[i]
    else:
        for i in range(len(text)):
            if not (text[i].isalnum() or text[i].isspace()) and unicodedata.category(text[i]) != "So":
                s += " "
            else:
                s += text[i]
    temp = s.split()
    return(" ".join(temp))
    
def normalize_repeating_chars(text, keep=1):
    """
        Input: A text and the number of keeps for the repeated letters
        Process: A letter repeated 3+ times in a row is cut to keep copies; doubles such as oo in good are left alone
        Output: Text after the modification
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    
    if len(text) == 0:
        return ""

    ans = []
    for c, g in groupby(text):
        count = len(list(g))
        if count >= 3:
            ans.append(c * keep)
        else:
            ans.append(c * count)

        return "".join(ans)


def remove_html(text: str) -> str:
    """
        Input: A string
        Process: Removes tags, then decodes entities with html.unescape
        Output: string without tags and with decoded entities
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")

    if len(text) == 0:
            return ""
    
    Tag = re.compile(r"<[^>]*>")

    s = Tag.sub(" ", text).strip() # -> to Remove Tags

    return html.unescape(s) # -> to decode entities

def remove_mentions(text: str) -> str:

    """
        Input: A string
        Process: @user handles, but not emails
        Output: A string without mentions
    """

    if not isinstance(text, str):
            raise TypeError(f"expected str, got {type(text).__name__}")
    
    if len(text) == 0:
            return ""

    Mentions = re.compile(r"(?<![A-Za-z0-9._%+-])@\w+(?:[.-]\w+)*")

    return Mentions.sub("", text).strip()

def remove_hashtags(text: str, keep_word: bool=False) -> str:
    """
        Input: A string and a boolean value to know if the word after the hashtag will be kept
        Process: remove the hashtags in the string with keep_word=True only the # goes
        Output: A string without hashtags
    """

    if not isinstance(text, str):
            raise TypeError(f"expected str, got {type(text).__name__}")
    
    if len(text) == 0:
            return ""

    Hashtags = re.compile(r"#(\w+)")

    if keep_word == True:
        return Hashtags.sub(r"\1", text)
        # (\w+) is a capturing group it remembers the tag word without the "#"
        # In keep_word=True \1 puts that saved word back in place of "#word"
    else:
        return Hashtags.sub("", text).strip()

def remove_digits(text: str) -> str:

    """
        Input: A string
        Process: Removes all the digits
        Output: A string without any digits
    """

    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    
    if len(text) == 0:
            return ""

    Digits = re.compile(r"\d+")

    # \d matches any Unicode digit such as Arabic-Indic ٠١٢٣ not only 0-9 if we make [0-9]+

    return Digits.sub("", text).strip()



            


    

