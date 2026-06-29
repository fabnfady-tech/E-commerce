from rest_framework import serializers
from .models import Category ,Product , Review
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        url = str(obj.image)
        # لو URL خارجي خليه زي ما هو
        if url.startswith('http://') or url.startswith('https://'):
            return url
        # لو ملف محلي ابني الـ URL كامل
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    class Meta:
        model = Product
        fields=['id','Category', 'title' , 'description','price', 'stock','is_available', 'created_at','image']
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer (many=True , read_only=True)
    class Meta :
        model = Category 
        fields =['id','name','slug','products']
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # بيعرض اسم اليوزر بس
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        extra_kwargs = {'product': {'read_only': True}}