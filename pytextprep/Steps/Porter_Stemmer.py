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

def _step1a(word: str) -> str:

    """ Returns the word after removing the letters that responsible for plural """

    if word.endswith("sses") or word.endswith("ies"):
        return word[:-2]
    elif word.endwith("ss"):
        return word
    elif word.endwith("s"):
        return word[:-1]
    return word


"""

STEP 1b:

    - if the suffix eed and m > 0 in the stem --> it becomes ee
        EX: agreed -> agree and need -> need
    - if the suffix ed and the stem has a vowel --> will be removed
    - if the suffix ing and the stem has a vowel --> will be removed

    If ed or ing was removed, fix the stem:
        - if it ends with at, bl or iz --> add e
            EX: troubled -> troubl -> trouble and realizing -> realiz -> realize
        - if it ends with a double consonant (not l, s or z) --> remove one letter
            Ex: planned -> plann -> plan and getting -> gett -> get and falling -> fall -> fall since the last letter is l
        - if m = 1 and it ends with CVC (cvc where the last is not w, x or y) --> add e
            Ex: hiding -> hid -> hide and caring -> car -> care

"""

def _step1b(word: str) -> str:

    """ Returns a string after removing the suffix ed or ing and fixes the stem """

    if word.endswith("eed"): 
        if _measure(word[:-3]) > 0:
            return word[:-1]
        return word

    removed = False
    if word.endswith("ed") and _has_vowel(word[:-2]):
        removed = True
        word = word[:-2]
    elif word.endswith("ing") and _has_vowel(word[:-3]):
        removed = True
        word = word[:-3]

    if removed:
        if word.endswith(("at", "bl", "iz")):
            return word + "e"
        elif _ends_double_consonant(word) and word[-1] not in "lsz":
            return word[:-1]
        elif _measure(word) == 1 and _ends_cvc(word):
            return word + "e"

    return word

"""

STEP 1c:

    - if the word ends with y and the stem has a vowel --> y becomes i
    - if the stem has no vowel --> nothing changed
        Ex: happy -> happi to match happiness -> happi and sky -> sky since the stem don't have a vowel

"""

def _step1c(word: str) -> str:

    """ Return a string after change the last letter if it 'y' to 'i' and nothing happened otherwise """

    if word[-1] == 'y' and _has_vowel(word[:-1]):
        return word[:-1] + "i"
    return word