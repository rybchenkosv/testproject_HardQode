from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from members.views import ProductViewSet, AccessibleProductViewSet, ProductStatsSerializerViewSet

router = routers.DefaultRouter()
router.register(r'api/product', ProductViewSet)
router.register(r'api/product_accessible', AccessibleProductViewSet)
router.register(r'api/product_stats', ProductStatsSerializerViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
