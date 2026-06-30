from django.shortcuts import render
from rest_framework import viewsets
from . models import Category,Product ,Review
from .serializers import CategorySerializer , ProductSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # ... بقية الفلاتر والـ backends بتاعتك ...

    # بنعمل كاش لصفحة عرض المنتجات لمدة دقيقتين (120 ثانية)
    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticatedOrReadOnly
    def get_queryset(self):
        # هنا بنقول للسيستم: هاتلي التقييمات التابعة للمنتج اللي رقمه في الـ URL فقط
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        # ده اللي بيمضي التقييم باسم اليوزر
        serializer.save(product_id=self.kwargs['product_pk'], user=self.request.user)# اللي مش مسجل يشوف بس، اللي مسجل يكتب
def home_dashboard(request):
    return render(request, 'index.html')
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'username و password مطلوبين'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'اليوزرنيم ده موجود بالفعل'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'تم إنشاء الحساب بنجاح'}, status=status.HTTP_201_CREATED)