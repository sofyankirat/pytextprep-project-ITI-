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