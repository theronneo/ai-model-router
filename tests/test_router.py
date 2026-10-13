import unittest

from src.router import choose_model


class FakeLaya:
    def __init__(self, choice):
        self.choice = choice
        self.state = None
        self.questions = None

    def predict(self, state, questions):
        self.state = state
        self.questions = questions
        return {
            "answers": {
                "model_tier": {
                    "type": "choice",
                    "choice": self.choice,
                    "probabilities": {"fast": 0.82, "strong": 0.18},
                    "confidence": 0.68,
                }
            },
            "routing": {"model": "english"},
        }


class RouterTests(unittest.TestCase):
    def test_fast_choice_maps_to_requested_codex_model(self):
        laya = FakeLaya("fast")

        result = choose_model("Rename this variable", laya, "gpt-6-luna", "gpt-6.1-sol")

        self.assertEqual(result["model"], "gpt-6-luna")
        self.assertEqual(result["tier"], "fast")
        self.assertEqual(laya.state, "Rename this variable")
        self.assertEqual(laya.questions["model_tier"]["type"], "choice")
        self.assertEqual(set(laya.questions["model_tier"]["criteria"]), {"fast", "strong"})

    def test_strong_choice_maps_to_requested_codex_model(self):
        result = choose_model("Design a migration", FakeLaya("strong"), "mini", "large")
        self.assertEqual(result["model"], "large")

    def test_blank_query_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "query must not be empty"):
            choose_model("   ", FakeLaya("fast"), "mini", "large")

    def test_unknown_choice_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unexpected Laya choice"):
            choose_model("A task", FakeLaya("unknown"), "mini", "large")


if __name__ == "__main__":
    unittest.main()
