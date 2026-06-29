from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. بنجيب سلة اليوزر
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "السلة غير موجودة!"}, status=status.HTTP_404_NOT_FOUND)

        items = cart.items.all()

        if not items.exists():
            return Response({"error": "السلة فارغة، أضف منتجات أولاً!"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. عملية النقل (Atomic transaction)
        with transaction.atomic():
            # حساب الإجمالي
            total = sum(item.total_price for item in items)
            
            # إنشاء الطلب
            order = Order.objects.create(user=request.user, total_price=total)

            # نقل المنتجات من السلة للطلب
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price # السعر وقت الشراء
                )
            
            # 3. تفريغ السلة بعد نجاح العملية
            cart.items.all().delete()

        return Response({"message": "تم إتمام الطلب بنجاح!", "order_id": order.id}, status=status.HTTP_201_CREATED)
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # بيجيب كل طلبات اليوزر الحالي بس
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)