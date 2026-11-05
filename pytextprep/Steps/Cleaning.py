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
        Process: replace the urls with the specified characters
        Output: the text after the replacement
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

