from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class ProductCategoryInfo(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()


class ProductInfo(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    quantity_in_stock = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    total_sold = serializers.IntegerField()
    excerpt = serializers.CharField()
    content = serializers.CharField()
    phone_number = serializers.CharField(allow_null=True, required=False)
    category = ProductCategoryInfo()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductListRequest(serializers.Serializer):
    category_id = serializers.UUIDField(required=False)
    search = serializers.CharField(required=False)
    ordering = serializers.CharField(required=False, default="id")


class ProductListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    products = ProductInfo(many=True)


class CategoryListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    categories = ProductCategoryInfo(many=True)


class ProductCreateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False, default="")
    price = serializers.IntegerField(min_value=0)
    quantity_in_stock = serializers.IntegerField(min_value=0)
    image = serializers.ImageField(required=False)
    excerpt = serializers.CharField(allow_blank=True, required=False, default="")
    content = serializers.CharField(allow_blank=True, required=False, default="")
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    category_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_quantity_in_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity in stock cannot be negative")
        return value

    def validate_image(self, value):
        if value and value.size > 2 * 1024 * 1024:  # 2MB
            raise serializers.ValidationError("Image size must be less than 2MB")
        return value


class ProductCreateResponse(serializers.Serializer):
    id = serializers.UUIDField()


class ProductDetailRequest(serializers.Serializer):
    id = serializers.UUIDField()


class ProductDetailResponse(ProductInfo):
    pass


class CategoryCreateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False, default="")


class CategoryCreateResponse(serializers.Serializer):
    id = serializers.UUIDField()


class CategoryDetailRequest(serializers.Serializer):
    id = serializers.UUIDField()


class CategoryDetailResponse(ProductCategoryInfo):
    pass
