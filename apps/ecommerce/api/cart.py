from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import Cart
from apps.ecommerce.serializers.cart import CartDetailRequest, CartDetailResponse
from common.exceptions import BadRequest
from common.serializers import ErrorResponse


@extend_schema(tags=["Cart"])
class CartDetailAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=CartDetailRequest,
        responses={
            200: CartDetailResponse,
            400: ErrorResponse,
            404: ErrorResponse,
            500: ErrorResponse
        }
    )
    def get(self, request, cart_id):
        """Get shopping cart details with items"""
        serializer = CartDetailRequest(data={
            **request.data,
            "cart_id": cart_id
        })
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        cart_id = serializer.validated_data.get("cart_id")
        cart = Cart.objects.filter(id=cart_id).prefetch_related("items__product").first()
        if not cart:
            raise BadRequest(404000, error_detail="Cart not found")

        # Calculate total price
        total_price = sum(item.quantity * item.product.price for item in cart.items.all())

        # Prepare response data
        response_data = {
            "id": cart.id,
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
            "items": cart.items.all(),
            "total_price": total_price
        }

        response = CartDetailResponse(response_data)
        return Response(response.data)
