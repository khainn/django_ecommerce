from rest_framework import serializers
from apps.ecommerce.models import Cart, CartItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'quantity_in_stock']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id']


class CartDetailRequest(serializers.Serializer):
    cart_id = serializers.UUIDField()


class CartDetailResponse(serializers.Serializer):
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    items = CartItemSerializer(many=True)
    total_price = serializers.IntegerField() 