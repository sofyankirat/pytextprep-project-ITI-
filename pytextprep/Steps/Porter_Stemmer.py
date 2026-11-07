def _is_consonant(word: str, i: int) -> bool:

    """ Returns True if the character is consonant and False otherwise """

    ch = word[i]
    if ch in "aieou":
        return False
    elif ch == 'y':
        if i == 0 or not _is_consonant(word, i - 1):
            return True
        else:
            return False
    return True

def _measure(stem: str) -> int:

    """ Returns the number of the VCs in the stem """

    m = 0
    prev_vowel = False
    for i in range(len(stem)):
        cons = _is_consonant(stem, i)
        if prev_vowel and cons:
            m += 1
        prev_vowel = not cons

    return m

def _has_vowel(stem: str) -> bool:

    """ Returns True if the stem has a vowel and False otherwise """

    for i in range(len(stem)):
        if not _is_consonant(stem, i):
            return True
    return False

def _ends_double_consonant(word: str) -> bool:

    """ Returns True if the word ends with double consonant and False otherwise """

    if len(word) >= 2 and word[-2] == word[-1] and _is_consonant(word, len(word) - 1):
        return True
    return False

def _ends_cvc(word: str) -> bool:

    """ Retuens True if the word ends with consonant, vowel and consonant and the last consonant not w,x,y and False otherwise """

    if len(word) >= 3 and _is_consonant(word, len(word) - 3) and not _is_consonant(word, len(word) - 2) and _is_consonant(word, len(word) - 1) and word[-1] not in "wxy":
        return True
    return False

""" 

STEP 1a: 

    - if the suffix sses --> it becomes ss
    - if the suffix ies --> it becomes i
    - if the suffix ss --> nothing changed
    - if the suffix s --> will be removed

"""

