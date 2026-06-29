from django.db import models
import hashlib
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class Category(models.Model):
    name=models.CharField(max_length=200 , verbose_name="اسم التصنيف")
    slug=models.SlugField(max_length=200,unique=True , verbose_name='الرابط الفرعي')
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Product(models.Model):
    Category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='products', verbose_name='التصنيف')
    title = models.CharField(max_length=255 , verbose_name='اسم المنتج' )
    description = models.TextField(blank=True , verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name='السعر') # عشان السعر بالقرش والجنيه
    stock = models.IntegerField(verbose_name='كمية المتاحة ') # الكمية المتاحة في المخزن
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الاضافة ')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    def __str__(self):
        return self.title
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    image_hash = models.CharField(max_length=64, unique=True, editable=False) # بصمة الصورة

    def save(self, *args, **kwargs):
        # 1. حساب البصمة (Hash) للصورة
        image_content = self.image.read()
        image_hash = hashlib.sha256(image_content).hexdigest()
        
        # 2. التأكد هل البصمة دي موجودة قبل كده؟
        if ProductImage.objects.filter(image_hash=image_hash).exists():
            raise ValidationError("هذه الصورة مرفوعة مسبقاً، لا يمكن تكرارها!")
        
        self.image_hash = image_hash
        super().save(*args, **kwargs)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # من 1 لـ 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"