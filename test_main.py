import unittest
from main import generate, score


class RobustnessTests(unittest.TestCase):
    def setUp(self):
        self.suite = generate([{"id": "a", "text": 'Cancel my "Trial"'}])

    def test_variations_are_deterministic(self):
        self.assertEqual(self.suite[0]["variants"]["casefold"], 'cancel my "trial"')
        self.assertIn("\u201d", self.suite[0]["variants"]["typographic_quotes"])
        self.assertEqual(self.suite, generate([{"id": "a", "text": 'Cancel my "Trial"'}]))

