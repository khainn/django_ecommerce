from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import Banner
from apps.ecommerce.serializers.banner import BannerSerializer
from common.serializers import ErrorResponse


@extend_schema(tags=["Banners"])
class BannerListAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        operation_id="banner_list",
        responses={200: BannerSerializer(many=True), 400: ErrorResponse, 500: ErrorResponse}
    )
    def get(self, request):
        """Get a list of active banners"""
        banners = Banner.objects.filter(is_active=True).order_by('position', '-created_at')
        serializer = BannerSerializer(banners, many=True, context={"request": request})
        return Response(serializer.data)
