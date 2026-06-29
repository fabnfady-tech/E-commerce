import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # البحث بالاسم (مش لازم تكتب الاسم كامل)
    name = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    # تحديد نطاق السعر
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte') # أكبر من أو يساوي
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte') # أقل من أو يساوي

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price']