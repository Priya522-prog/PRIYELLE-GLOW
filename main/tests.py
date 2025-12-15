from django.test import TestCase
from .utils import analyze_image

class AnalyzeImageTest(TestCase):
    def test_analysis(self):
        result = analyze_image("sample.jpg")
        self.assertIn("skin_type", result)
        self.assertIn("skincare", result)
        self.assertIn("makeup", result)
