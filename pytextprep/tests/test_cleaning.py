import unittest

from pytextprep.Steps.Cleaning import (
    lowercase, normalize_whitespace, remove_urls, remove_emails,
    remove_punctuation, normalize_repeating_chars, remove_html,
    remove_mentions, remove_hashtags, remove_digits, handle_emojis,
)

ALL_FUNCS = [
    lowercase, normalize_whitespace, remove_urls, remove_emails,
    remove_punctuation, normalize_repeating_chars, remove_html,
    remove_mentions, remove_hashtags, remove_digits, handle_emojis,
]


class TestEdgeInputs(unittest.TestCase):

    def test_empty_string(self):                      # case 1
        for func in ALL_FUNCS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(""), "")

    def test_wrong_type(self):                        # case 2
        for func in ALL_FUNCS:
            for value, type_name in ((None, "NoneType"), (42, "int")):
                with self.subTest(func=func.__name__, value=value):
                    with self.assertRaisesRegex(TypeError, type_name):
                        func(value)

class TestCleaning(unittest.TestCase):

    def test_remove_urls_trailing_dot(self):          # case 3
        self.assertEqual(remove_urls("go to https://a.io/x?y=1."), "go to .")

    def test_remove_urls_broken(self):                # case 4
        text = "not a url: http:/broken"
        self.assertEqual(remove_urls(text), text)

    def test_remove_emails(self):                     # case 5
        self.assertEqual(remove_emails("write to ali@iti.gov.eg today"), "write to today")

    def test_repeating_chars_keeps_doubles(self):     # case 6
        self.assertEqual(normalize_repeating_chars("good book"), "good book")

    def test_repeating_chars_keep_2(self):            # case 7
        self.assertEqual(normalize_repeating_chars("sooo", keep=2), "soo")

    def test_remove_punctuation_apostrophes(self):    # case 11
        self.assertEqual(remove_punctuation("rock'n'roll!!"), "rocknroll")

    def test_lowercase(self):
        self.assertEqual(lowercase("NLP Rocks"), "nlp rocks")

    def test_normalize_whitespace(self):
        self.assertEqual(normalize_whitespace("  a\t\tb\n c "), "a b c")


if __name__ == "__main__":
    unittest.main()