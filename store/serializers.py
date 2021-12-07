from decimal import Decimal
from rest_framework import serializers
from .models import Cart, Product, Collection, Review, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax',
                  'collection']
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.16)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'unit_price', 'price_with_tax']
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.16)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description', 'product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total = serializers.SerializerMethodField(
        method_name='caculate_total_price')

    def caculate_total_price(self, cartitem):
        return cartitem.product.unit_price * cartitem.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitems = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField(
        method_name='get_cart_total')

    def get_cart_total(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.cartitems.all()])

    class Meta:
        model = Cart
        fields = ['id', 'cartitems', 'cart_total']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        product_id = self.validated_data.get('product_id')
        quantity = self.validated_data.get('quantity')
        cart_id = self.context.get('cart_id')
        try:
            cart_item = CartItem.objects.get(
                product_id=product_id, cart_id=cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
