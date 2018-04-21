from manager import models as cmod
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    Category = serializers.StringRelatedField()
    class Meta:
        model = cmod.Product
        fields = ('Name','Category','Price')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cmod.Category
        fields = ('Name','Description')
