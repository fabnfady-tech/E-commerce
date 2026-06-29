from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # <--- ضيف السطر ده فوق
from .models import Cart, CartItem
from .serializers import CartSerializer
from store.models import Product

class CartView(APIView):
    permission_classes = [IsAuthenticated]  # <--- ضيف السطر ده جوه الكلاس

    def get(self, request):
        # سيب كود الـ get زي ما هو بالظبط
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        # سيب كود الـ post زي ما هو بالظبط
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        return Response({"message": "تمت إضافة المنتج للسلة!"}, status=status.HTTP_201_CREATED)