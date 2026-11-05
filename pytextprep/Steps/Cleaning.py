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
        raise TypeError(f"expected str, got {isinstance(s).__name__}")

    if len(s) == 0:
            print("")

    temp = s.strip()
    temp2 = ""
    for i in range(len(s)):
        if temp[i] < " ":
            temp2 += " "
        else:
            temp2 += temp[i]
            
    ans = ""

    for i in range(len(temp2)):
        if temp2[i] == " " and temp2[i + 1] == " ":
            continue
        ans += temp2[i]

    return ans