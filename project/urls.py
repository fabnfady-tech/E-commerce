from django.contrib import admin
from django.urls import path, include
from project import settings
from store.views import home_dashboard
from django.conf.urls.static import static
from store.views import home_dashboard, register_view 
# 🌟 استيراد مسارات الـ JWT الجديدة للـ Login وتجديد التوكن
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_dashboard, name='home'),
    path('', include('store.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', register_view, name='register'),
    
    # 🔐 روابط الـ JWT الاحترافية
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)