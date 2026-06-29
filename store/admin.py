from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 🛠️ صلحنا هنا 'category' بقت سمول عشان تطابق الموديل
    list_display = ['id', 'title', 'Category', 'price', 'stock', 'is_available', 'created_at','image']
    
    # 🛠️ وهنا كمان بقت سمول category
    list_filter = ['is_available', 'Category', 'created_at']
    
    list_editable = ['price', 'stock', 'is_available']
    
    # ❌ شيلنا سطر الـ prepopulated_fields خالص من هنا لأن الـ Product معندوش slug
    
    search_fields = ['title', 'description']