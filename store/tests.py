from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        # ضفنا حقل الـ stock هنا عشان قاعدة البيانات توافق على إنشاء المنتج
        self.product = Product.objects.create(
            title="آيفون 15",
            price=1000.00,
            stock=10  # <--- السطر ده هو اللي هيحل المشكلة بالظبط!
        )

    def test_product_creation(self):
        # بنختبر الحقول للتأكد إنها اتخزنت صح
        self.assertEqual(self.product.title, "آيفون 15")
        self.assertEqual(self.product.price, 1000.00)
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(isinstance(self.product, Product))