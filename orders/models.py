
# Create your models here.
from django.conf import settings
from django.db import models
from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # Pending, Completed, Cancelled
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"طلب رقم {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # السعر وقت الشراء

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"