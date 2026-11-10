import unittest
from pytextprep import Pipeline
from pytextprep.exceptions import InvalidStepParamsError
from pytextprep.Steps.remove_accents import remove_accents

class TestRemoveAccents(unittest.TestCase):

    def test_basic_accents(self):
        self.assertEqual(remove_accents("café"), "cafe")
        self.assertEqual(remove_accents("naïve"), "naive")
        self.assertEqual(remove_accents("señor"), "senor")

    def test_several_accents_in_a_sentence(self):
        self.assertEqual(remove_accents("Crème Brûlée"), "Creme Brulee")

    def test_capitals_are_kept(self):
        self.assertEqual(remove_accents("ÉCOLE"), "ECOLE")

    def test_special_forms_become_plain(self):
        self.assertEqual(remove_accents("\u2460\u2461\u2462"), "123")   # ①②③
        self.assertEqual(remove_accents("\ufb01ne"), "fine")            # ligature ﬁ
        self.assertEqual(remove_accents("x\u00b2"), "x2")               # x²

    def test_plain_text_unchanged(self):
        text = "Hello, World! 123"
        self.assertEqual(remove_accents(text), text)

    def test_idempotent(self):
        once = remove_accents("Crème Brûlée")
        self.assertEqual(remove_accents(once), once)

    def test_empty_string(self):                       # case 1
        self.assertEqual(remove_accents(""), "")

    def test_wrong_type(self):                         # case 2
        for value, type_name in ((None, "NoneType"), (42, "int")):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, type_name):
                    remove_accents(value)


class TestRemoveAccentsInPipeline(unittest.TestCase):

    def test_registered_as_step(self):
        p = Pipeline([("remove_accents", {})])
        self.assertEqual(p.transform("café"), "cafe")

    def test_after_lowercase(self):
        p = Pipeline([("lowercase", {}), ("remove_accents", {})])
        self.assertEqual(p.transform("CAFÉ"), "cafe")

    def test_unknown_parameter_rejected(self):
        with self.assertRaises(InvalidStepParamsError):
            Pipeline([("remove_accents", {"keep": True})])


if __name__ == "__main__":
    unittest.main()