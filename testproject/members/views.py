from rest_framework import viewsets
from .models import Product, Lesson
from .serializers import ProductSerializer, AccessibleProductSerializer, ProductStatsSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AccessibleProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AccessibleProductSerializer

class ProductStatsSerializerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer

