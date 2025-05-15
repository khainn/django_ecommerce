from rest_framework import serializers

from apps.ecommerce.models import Product


class OrderItemRequest(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateRequest(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=20)
    customer_address = serializers.CharField()
    items = OrderItemRequest(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        
        # Check for duplicate products
        product_ids = [item['product_id'] for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products are not allowed")
        
        # Verify products exist and have enough stock
        product_ids = [item['product_id'] for item in items]
        existing_products = Product.objects.filter(id__in=product_ids)
        existing_product_ids = {product.id for product in existing_products}

        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            if product_id not in existing_product_ids:
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist")
            product = next((p for p in existing_products if p.id == product_id), None)
            if product and product.quantity_in_stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product.name}. Available: {product.quantity_in_stock}"
                )
        return items


class OrderCreateResponse(serializers.Serializer):
    id = serializers.UUIDField()
    cart_id = serializers.UUIDField()
