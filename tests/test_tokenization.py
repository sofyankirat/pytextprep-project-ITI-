import unittest

from pytextprep.Steps.Tokenization import (
    word_tokenize, sent_tokenize, remove_stopwords, expand_contractions,
)


class TestTokenization(unittest.TestCase):

    def test_empty_inputs(self):                      # case 1
        self.assertEqual(word_tokenize(""), [])
        self.assertEqual(sent_tokenize(""), [])
        self.assertEqual(remove_stopwords(""), "")
        self.assertEqual(expand_contractions(""), "")

    def test_wrong_type(self):                        # case 2
        for func in (word_tokenize, sent_tokenize, remove_stopwords, expand_contractions):
            for value, type_name in ((None, "NoneType"), (42, "int")):
                with self.subTest(func=func.__name__, value=value):
                    with self.assertRaisesRegex(TypeError, type_name):
                        func(value)

    def test_curly_apostrophe(self):                  # case 8
        self.assertEqual(expand_contractions("They’re here"), "They are here")

    def test_stopwords_case_insensitive(self):        # case 9
        self.assertEqual(remove_stopwords("THE end"), "end")

    def test_sent_tokenize(self):                     # case 10
        self.assertEqual(
            sent_tokenize("Pi is 3.14. Use e.g. this one!"),
            ["Pi is 3.14.", "Use e.g. this one!"],
        )

    def test_word_tokenize(self):
        self.assertEqual(
            word_tokenize("State-of-the-art NLP, isn't it?"),
            ["State-of-the-art", "NLP", "isn't", "it"],
        )


if __name__ == "__main__":
    unittest.main()