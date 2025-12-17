from django.test import TestCase
from .utils import analyze_image

class AnalyzeImageTest(TestCase): 
    def test_analysis(self):
        result = analyze_image("sample.jpg")
        self.assertIn("skin_type", result)
        self.assertIn("skincare", result)
        self.assertIn("makeup", result)

class ProductListingTest(TestCase):
    def test_analysis_results_shows_products_matching_skin_type(self):
        from django.contrib.auth.models import User
        from django.urls import reverse
        from .models import Product, SkinAnalysis

        # create a user and log in
        user = User.objects.create_user(username='tester', password='pass')
        self.client.login(username='tester', password='pass')

        # create a product that matches skin type 'oily' and category 'skincare'
        prod = Product.objects.create(
            name='Test Oil Control',
            description='For oily skin',
            price=10.00,
            category='skincare',
            skin_type='oily'
        )

        # create a skin analysis with matching skin_type
        analysis = SkinAnalysis.objects.create(
            user=user,
            image='analysis/sample.jpg',
            skin_type='oily'
        )

        url = reverse('analysis_results', args=[analysis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # the response should contain the product name
        self.assertContains(response, 'Test Oil Control')

class RegisterViewTest(TestCase):
    def test_register_creates_user_with_matching_passwords(self):
        from django.urls import reverse
        from django.contrib.auth.models import User

        # submit registration with matching passwords
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        })
        # should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

class AnalyzeFlowTest(TestCase):
    def test_posting_captured_image_creates_analysis(self):
        from django.urls import reverse
        from django.contrib.auth.models import User
        from .models import SkinAnalysis

        user = User.objects.create_user(username='tester2', password='pass')
        self.client.login(username='tester2', password='pass')

        # minimal 1x1 PNG data URI
        data_uri = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII='

        response = self.client.post(reverse('analyze'), data={'captured_image': data_uri})
        # should redirect to results page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SkinAnalysis.objects.filter(user=user).exists())
