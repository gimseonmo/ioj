from django.test import SimpleTestCase

from .services.providers import normalize_gemini_model


class GeminiModelNormalizeTest(SimpleTestCase):
    def test_legacy_15_model_uses_low_cost_default(self):
        self.assertEqual(normalize_gemini_model("gemini-1.5-flash"), "gemini-2.5-flash-lite")
        self.assertEqual(normalize_gemini_model("gemini-1.5-pro"), "gemini-2.5-flash-lite")

    def test_current_model_is_preserved(self):
        self.assertEqual(normalize_gemini_model("gemini-2.5-flash-lite"), "gemini-2.5-flash-lite")
