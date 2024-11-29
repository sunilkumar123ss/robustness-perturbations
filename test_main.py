import unittest
from main import generate, score


class RobustnessTests(unittest.TestCase):
    def setUp(self):
        self.suite = generate([{"id": "a", "text": 'Cancel my "Trial"'}])

    def test_variations_are_deterministic(self):
        self.assertEqual(self.suite[0]["variants"]["casefold"], 'cancel my "trial"')
        self.assertIn("\u201d", self.suite[0]["variants"]["typographic_quotes"])
        self.assertEqual(self.suite, generate([{"id": "a", "text": 'Cancel my "Trial"'}]))

    def test_changed_and_missing_are_distinct(self):
        result = score(self.suite, [{"id": "a", "baseline_output": "cancel",
                                    "variants": {"casefold": " cancel ", "whitespace": "other"}}])
        self.assertEqual((result["tested"], result["missing"], result["stable"]), (2, 1, 1))
        self.assertEqual(result["exact_output_stability"], 0.5)
        self.assertAlmostEqual(result["coverage"], 2 / 3)

