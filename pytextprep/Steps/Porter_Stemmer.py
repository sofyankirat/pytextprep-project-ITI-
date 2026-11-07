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
    elif word.endswith("ss"):
        return word
    elif word.endswith("s"):
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

def _apply_rules(word: str, rules: dict, min_m: int) -> str:

    """ Applies the longest matching suffix rule if the stem has m > min_m """

    for suffix in sorted(rules, key=len, reverse=True):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if _measure(stem) > min_m:
                return stem + rules[suffix]
            return word
    return word

def _step2(word: str) -> str:

    STEP2 = {
        "ational": "ate", "tional": "tion", "enci": "ence", "anci": "ance",
        "izer": "ize", "abli": "able", "alli": "al", "entli": "ent",
        "eli": "e", "ousli": "ous", "ization": "ize", "ation": "ate",
        "ator": "ate", "alism": "al", "iveness": "ive", "fulness": "ful",
        "ousness": "ous", "aliti": "al", "iviti": "ive", "biliti": "ble",
    }

    # EX: Relational --> Relate
    
    return _apply_rules(word, STEP2, 0)

def _step3(word: str) -> str:

    STEP3 = {
        "icate": "ic", "ative": "", "alize": "al", "iciti": "ic",
        "ical": "ic", "ful": "", "ness": "",
    }

    # EX: happiness --> happi

    return _apply_rules(word, STEP3, 0)

def _step4(word: str) -> str:

    STEP4 = (
        "al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement",
        "ment", "ent", "ion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"
    )

    for suffix in sorted(STEP4, key=len, reverse=True):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if _measure(stem) > 1:
                # stem[-1] IndexError: string index out of range if the stem is empty and stem[-1:] return empty string
                if suffix == "ion" and stem[-1:] not in ("t", "s"):
                    return word
                return stem
            return word

    # EX: adjustment --> adjust and region --> region since m = 1 not bigger than 1
    
    return word

"""

STEP 5a:

    - if the word ends with e, look at the stem (the word without the final e)
    - if m > 1 in the stem --> remove the e
        EX: probate -> probat
    - if m = 1 and the stem does not end with CVC --> remove the e
        EX: cease -> ceas
    - if m = 1 and the stem ends with CVC --> keep the e
        EX: rate -> rate (removing it would give rat, a different word)
    - if m = 0 --> nothing changed
        EX: the -> the

"""

def _step5a(word: str) -> str:

    """ Returns the word after removing the final e if the stem is long enough (m > 1) or if m = 1 and the stem doesn't end with CVC """

    if word.endswith("e"):
        stem = word[:-1]
        if _measure(stem) > 1 or (_measure(stem) == 1 and not _ends_cvc(stem)):
            return stem
    return word

"""

STEP 5b:

    - if m > 1 and the word ends with ll --> remove one l
        EX: controll -> control
    - if m <= 1 --> nothing changed
        EX: roll -> roll and fall -> fall
    - m is measured on the whole word (including the ll), not on the stem

"""

def _step5b(word: str) -> str:

    """ Returns the word after removing one l from a final double l if m > 1 """

    if word.endswith("ll") and _measure(word) > 1:
        return word[:-1]
    return word


