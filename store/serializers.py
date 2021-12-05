from decimal import Decimal
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection = StringRelatedField()
    collection1 = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        source='collection'
    )
    collection2 = CollectionSerializer(source='collection')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.16)
