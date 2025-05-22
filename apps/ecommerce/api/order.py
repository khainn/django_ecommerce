from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import Cart, CartItem, Order, Product
from apps.ecommerce.serializers.order import OrderCreateRequest, OrderCreateResponse
from common.exceptions import BadRequest
from common.serializers import ErrorResponse


@extend_schema(tags=["Orders"])
class OrderCreateAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    @extend_schema(
        request=OrderCreateRequest,
        responses={
            201: OrderCreateResponse,
            400: ErrorResponse,
            500: ErrorResponse
        }
    )
    @transaction.atomic
    def post(self, request):
        """Create a new order with cart and items"""
        serializer = OrderCreateRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        validated_data = serializer.validated_data
        items_data = validated_data.pop("items")

        try:
            # Step 1: Create a new cart
            cart = Cart.objects.create()

            # Step 2: Create cart items
            total_price = 0
            for item_data in items_data:
                product_id = item_data["product_id"]
                quantity = item_data["quantity"]

                product = Product.objects.get(id=product_id)

                # Create cart item
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )

                # Update product stock
                product.quantity_in_stock -= quantity
                product.total_sold = (product.total_sold or 0) + quantity
                product.save()

                # Add to total price
                total_price += product.price * quantity

            # Step 3: Create the order
            order = Order.objects.create(
                customer_name=validated_data["customer_name"],
                customer_phone=validated_data["customer_phone"],
                customer_email=validated_data.get("customer_email", ""),
                customer_address=validated_data["customer_address"],
                notes=validated_data.get("notes", ""),
                total_price=total_price,
                cart=cart
            )

            # Return response
            response = OrderCreateResponse({
                "id": order.id,
                "cart_id": cart.id
            })
            return Response(response.data, status=201)

        except Exception as e:
            # In case of error, the transaction will be rolled back
            if isinstance(e, BadRequest):
                raise e
            raise BadRequest(500000, error_detail=str(e)) from e
