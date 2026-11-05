def lowercase(s: str) -> str:
    """
        Input: A string
        Process: transform the uppercase letters to the lowercase letters
        Output: A string with lowercase letters
    """

    if not isinstance(s, str):
        raise TypeError(f"expected str, got {isinstance(s)}")

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
            raise TypeError(f"expected str, got {isinstance(s)}")

    if len(s) == 0:
            return ""

    ans = s.strip()
    for i in range(len(s)):
        if s[i] < 32:
            ans = s.replace(s[i], " ")
             



