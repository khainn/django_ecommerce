from rest_framework import serializers

from apps.ecommerce.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model"""
    class Meta:
        model = Banner
        fields = ["id", "title", "image", "target_url", "position", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
