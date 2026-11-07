import unittest

from pytextprep.Steps.Porter_Stemmer import stem


class TestStem(unittest.TestCase):

    def test_examples(self):
        cases = {
            "running": "run", "caresses": "caress", "ponies": "poni",
            "relational": "relat", "connected": "connect",
        }
        for word, expected in cases.items():
            with self.subTest(word=word):
                self.assertEqual(stem(word), expected)

    def test_empty_and_wrong_type(self):
        self.assertEqual(stem(""), "")
        with self.assertRaisesRegex(TypeError, "NoneType"):
            stem(None)
        with self.assertRaisesRegex(TypeError, "int"):
            stem(42)


if __name__ == "__main__":
    unittest.main()