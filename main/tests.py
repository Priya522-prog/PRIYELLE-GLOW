from django.test import TestCase
from .utils import analyze_image

class AnalyzeImageTest(TestCase):
    def test_analysis(self):
        result = analyze_image("sample.jpg")
        self.assertIn("skin_type", result)
        self.assertIn("skincare", result)
        self.assertIn("makeup", result)


class DashboardCaptureTest(TestCase):
    def test_dashboard_post_creates_analysis_and_redirects(self):
        from django.contrib.auth.models import User
        from django.urls import reverse

        user = User.objects.create_user(username='tester', password='pass')
        self.client.login(username='tester', password='pass')

        # minimal valid base64 image (1x1 PNG)
        img_b64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAn8B9mY6mAAAAABJRU5ErkJggg=='

        response = self.client.post(reverse('dashboard'), data={'captured_image': img_b64})
        # should redirect to analysis_results
        self.assertEqual(response.status_code, 302)
        # analysis created
        from .models import SkinAnalysis
        self.assertTrue(SkinAnalysis.objects.filter(user=user).exists())