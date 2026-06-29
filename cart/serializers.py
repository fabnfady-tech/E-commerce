from rest_framework import serializers
from .models import Cart, CartItem
from store.serializers import ProductSerializer  # هنفترض إنك عامل سيرياليزر للمنتج

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # عشان يظهر تفاصيل المنتج
    total_price = serializers.ReadOnlyField()   # عشان يظهر السعر المحسوب أوتوماتيك

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True) # عشان يجيب كل الأصناف اللي جوه السلة
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']