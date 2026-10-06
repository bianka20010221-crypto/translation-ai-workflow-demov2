import unittest

from app.models import TranslationRequest
from app.workflow import WorkflowService


class WorkflowTests(unittest.TestCase):
    def test_technical_en_de_selects_specialist(self):
        request = TranslationRequest("T1", "Demo", "en", "de", 2000, "Technical manual", 48)
        result = WorkflowService().run(request)
        self.assertEqual(result["classification"]["domain"], "technical")
        self.assertEqual(result["assignment"]["linguist"]["name"], "Elena Petrova")
        self.assertFalse(result["manual_review_required"])

    def test_unknown_pair_requires_manual_review(self):
        request = TranslationRequest("T2", "Demo", "en", "fr", 100, "General note", 48)
        result = WorkflowService().run(request)
        self.assertIsNone(result["assignment"])
        self.assertTrue(result["manual_review_required"])

    def test_rejects_invalid_request(self):
        request = TranslationRequest("T3", "Demo", "en", "en", 100, "General", 48)
        with self.assertRaises(ValueError):
            WorkflowService().run(request)


if __name__ == "__main__":
    unittest.main()
