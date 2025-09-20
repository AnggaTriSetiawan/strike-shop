from django.test import TestCase, Client
from .models import Product

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_product_creation(self):
        product = Product.objects.create(
          title="BURHAN FC MENANG",
          content="BURHAN FC 1-0 PANDA BC",
          category="match",
          product_views=1001,
          is_featured=True
        )
        self.assertTrue(product.is_product_hot)
        self.assertEqual(product.category, "match")
        self.assertTrue(product.is_featured)
        
    def test_product_default_values(self):
        product = Product.objects.create(
          title="Test product",
          content="Test content"
        )
        self.assertEqual(product.category, "update")
        self.assertEqual(product.views, 0)
        self.assertFalse(product.is_featured)
        
    def test_increment_views(self):
        product = Product.objects.create(
          title="Test product",
          content="Test content"
        )
        initial_views = product.views
        product.increment_views()
        self.assertEqual(product.views, initial_views + 1)
