from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import Product, ProductCategory
from common.exceptions import BadRequest
from common.serializers import ErrorResponse
from apps.ecommerce.serializers.product import (
    ProductListRequest, 
    ProductListResponse,
    ProductDetailResponse,
    CategoryListResponse,
)


@extend_schema(tags=['Products'])
class ProductListAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(parameters=[ProductListRequest],
                   responses={200: ProductListResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        """Get a list of products with optional filtering"""
        serializer = ProductListRequest(data=request.query_params.dict())
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        # Get filter parameters
        category_id = serializer.validated_data.get('category_id')
        search = serializer.validated_data.get('search')
        ordering = serializer.validated_data.get('ordering', '-created_at')

        # Build query
        products_query = Product.objects.all().select_related('category')
        
        # Apply filters
        if category_id:
            products_query = products_query.filter(category_id=category_id)
        
        if search:
            products_query = products_query.filter(name__icontains=search)
            
        # Apply ordering
        products_query = products_query.order_by(ordering)
        
        # Prepare response
        response = ProductListResponse({
            'count': products_query.count(),
            'products': products_query
        }, context={'request': request})
        return Response(response.data)


@extend_schema(tags=['Products'])
class ProductDetailAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    
    @extend_schema(responses={200: ProductDetailResponse, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
    def get(self, request, product_id):
        """Get product details"""
        product = Product.objects.filter(id=product_id).select_related('category').first()
        if not product:
            raise BadRequest(404000, error_detail="Product not found")
        
        response = ProductDetailResponse(product, context={'request': request})
        return Response(response.data)


@extend_schema(tags=['Categories'])
class CategoryListAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    @extend_schema(responses={200: CategoryListResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        """Get a list of product categories"""
        # Get filter parameters
        search = request.query_params.get('search')
        
        # Build query
        categories_query = ProductCategory.objects.all()
        
        # Apply filters
        if search:
            categories_query = categories_query.filter(name__icontains=search)
            
        # Prepare response
        response = CategoryListResponse({
            'count': categories_query.count(),
            'categories': categories_query
        }, context={'request': request})
        return Response(response.data)
