import unittest

from pytextprep import Pipeline
from pytextprep.exceptions import InvalidStepParamsError
from pytextprep.Steps.normalize_arabic import normalize_arabic   


class TestNormalizeArabic(unittest.TestCase):

    def test_remove_tashkeel(self):
        self.assertEqual(normalize_arabic("مُحَمَّدٌ"), "محمد")

    def test_alef_variants(self):
        self.assertEqual(normalize_arabic("أحمد"), "احمد")
        self.assertEqual(normalize_arabic("إسلام"), "اسلام")
        self.assertEqual(normalize_arabic("آمن"), "امن")

    def test_remove_tatweel(self):
        self.assertEqual(normalize_arabic("كبيـــــر"), "كبير")

    def test_alef_maksura_to_yaa(self):
        self.assertEqual(normalize_arabic("على"), "علي")

    def test_superscript_alef_removed(self):
        self.assertEqual(normalize_arabic("\u0647\u0670\u0630\u0627"), "\u0647\u0630\u0627")

    def test_all_tashkeel_range(self):
        marks = "".join(chr(c) for c in range(0x064B, 0x0653))
        self.assertEqual(normalize_arabic("تم" + marks + "ام"), "تمام")

    def test_taa_marbuta_default_unchanged(self):
        self.assertEqual(normalize_arabic("مدرسة"), "مدرسة")

    def test_taa_marbuta_true(self):
        self.assertEqual(normalize_arabic("مدرسة", taa_marbuta=True), "مدرسه")

    def test_non_arabic_text_unchanged(self):
        self.assertEqual(normalize_arabic("Hello 123!"), "Hello 123!")

    def test_mixed_text(self):
        self.assertEqual(normalize_arabic("Hi أَحْمَد"), "Hi احمد")

    def test_idempotent(self):
        once = normalize_arabic("مُحَمَّدٌ كبيـــر")
        self.assertEqual(normalize_arabic(once), once)

    def test_empty_string(self):                      # case 1
        self.assertEqual(normalize_arabic(""), "")

    def test_wrong_type(self):                        # case 2
        for value, type_name in ((None, "NoneType"), (42, "int")):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, type_name):
                    normalize_arabic(value)


class TestNormalizeArabicInPipeline(unittest.TestCase):

    def test_works_as_a_step(self):
        p = Pipeline([("normalize_arabic", {})])
        self.assertEqual(p.transform("أَحْمَد"), "احمد")

    def test_step_with_param(self):
        p = Pipeline([("normalize_arabic", {"taa_marbuta": True})])
        self.assertEqual(p.transform("مدرسة"), "مدرسه")

    def test_bad_param_name(self):
        with self.assertRaises(InvalidStepParamsError) as ctx:
            Pipeline([("normalize_arabic", {"taa": True})])
        self.assertIn("taa", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()