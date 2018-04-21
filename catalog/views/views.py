from django.contrib.auth.models import User, Group
from manager import models as cmod
from rest_framework import viewsets
from catalog.views.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = cmod.Product.objects.all().order_by('Category','Name')
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = cmod.Category.objects.all()
    serializer_class = CategorySerializer
