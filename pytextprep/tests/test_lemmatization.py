import unittest

from pytextprep.Steps.lemmatization import lemmatize


class TestLemmatize(unittest.TestCase):

    def test_table_example(self):
        self.assertEqual(lemmatize("emails studies classes bus"), "email study class bus")

    def test_irregular(self):
        self.assertEqual(lemmatize("children went"), "child go")

    def test_empty_and_wrong_type(self):
        self.assertEqual(lemmatize(""), "")
        with self.assertRaisesRegex(TypeError, "NoneType"):
            lemmatize(None)
        with self.assertRaisesRegex(TypeError, "int"):
            lemmatize(42)


if __name__ == "__main__":
    unittest.main()