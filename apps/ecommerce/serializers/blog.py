from rest_framework import serializers


class BlogImageInfo(serializers.Serializer):
    id = serializers.UUIDField()
    image = serializers.SerializerMethodField()
    caption = serializers.CharField()
    display_order = serializers.IntegerField()

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class BlogInfo(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    slug = serializers.SlugField()
    author = serializers.CharField()
    date = serializers.DateField()
    image = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    excerpt = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_gallery(self, obj):
        # Only include gallery in detail view
        if not hasattr(obj, "gallery"):
            return []

        gallery_images = obj.gallery.all()
        serializer = BlogImageInfo(gallery_images, many=True, context=self.context)
        return serializer.data


class BlogListRequest(serializers.Serializer):
    search = serializers.CharField(required=False)
    ordering = serializers.CharField(required=False, default="-date")


class BlogListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    blogs = BlogInfo(many=True)


class BlogDetailRequest(serializers.Serializer):
    slug = serializers.SlugField()


class BlogDetailResponse(BlogInfo):
    pass
