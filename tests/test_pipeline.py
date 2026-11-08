import unittest

from pytextprep import Pipeline
from pytextprep.exceptions import UnknownStepError, InvalidStepParamsError
from pytextprep.registry import register_step, available_steps


class TestPipeline(unittest.TestCase):

    def test_empty_pipeline_changes_nothing(self):    # case 12
        self.assertEqual(Pipeline([]).transform("  Hi  "), "  Hi  ")

    def test_unknown_step_suggestion(self):           # case 13
        with self.assertRaises(UnknownStepError) as ctx:
            Pipeline([("remove_url", {})])
        self.assertIn("remove_urls", str(ctx.exception))

    def test_transform_batch(self):                   # case 14
        p = Pipeline([("lowercase", {})])
        self.assertEqual(p.transform_batch(["A", "", "B"]), ["a", "", "b"])

    def test_no_hidden_state(self):                   # case 15
        p = Pipeline([("lowercase", {}), ("remove_punctuation", {}), ("stem", {})])
        text = "Running, RUNNING!"
        self.assertEqual(p.transform(text), p.transform(text))

    def test_wrong_type(self):                        # case 2
        for value, type_name in ((None, "NoneType"), (42, "int")):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, type_name):
                    Pipeline([]).transform(value)

    def test_invalid_params(self):
        with self.assertRaises(InvalidStepParamsError) as ctx:
            Pipeline([("remove_punctuation", {"keep_emoji": False})])
        self.assertIn("keep_emoji", str(ctx.exception))

    def test_steps_and_return_tokens(self):
        p = Pipeline([("lowercase", {})])
        self.assertEqual(p.steps, [("lowercase", {})])
        self.assertEqual(p.transform("A B", return_tokens=True), ["a", "b"])

    def test_available_steps(self):
        self.assertIn("lowercase", available_steps())

    def test_register_custom_step(self):
        @register_step("_test_exclaim")
        def exclaim(text):
            return text + "!"

        self.assertIn("_test_exclaim", available_steps())
        self.assertEqual(Pipeline([("_test_exclaim", {})]).transform("hi"), "hi!")


if __name__ == "__main__":
    unittest.main()