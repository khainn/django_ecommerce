from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import Blog
from apps.ecommerce.serializers.blog import (
    BlogDetailResponse,
    BlogListRequest,
    BlogListResponse,
)
from common.exceptions import BadRequest
from common.serializers import ErrorResponse


@extend_schema(tags=["Blogs"])
class BlogListAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(parameters=[BlogListRequest],
                   responses={200: BlogListResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        """Get a list of blogs with optional filtering"""
        serializer = BlogListRequest(data=request.query_params.dict())
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        # Get filter parameters
        search = serializer.validated_data.get("search")
        ordering = serializer.validated_data.get("ordering", "-date")

        # Build query
        blogs_query = Blog.objects.all()

        # Apply filters
        if search:
            blogs_query = blogs_query.filter(title__icontains=search)

        # Apply ordering
        blogs_query = blogs_query.order_by(ordering)

        # Prepare response
        response = BlogListResponse({
            "count": blogs_query.count(),
            "blogs": blogs_query
        }, context={"request": request})
        return Response(response.data)


@extend_schema(tags=["Blogs"])
class BlogDetailAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(responses={200: BlogDetailResponse, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
    def get(self, request, slug):
        """Get blog details by slug"""
        blog = Blog.objects.filter(slug=slug).prefetch_related("gallery").first()
        if not blog:
            raise BadRequest(404000, error_detail="Blog not found")

        response = BlogDetailResponse(blog, context={"request": request})
        return Response(response.data)
