from django.urls import path

from apps.ecommerce.api.blog import BlogDetailAPIView, BlogListAPIView
from apps.ecommerce.api.cart import CartDetailAPIView
from apps.ecommerce.api.order import OrderCreateAPIView
from apps.ecommerce.api.product import CategoryListAPIView, ProductDetailAPIView, ProductListAPIView

urlpatterns = [
    # Product URLs
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<uuid:product_id>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),

    # Cart URLs
    path("carts/<uuid:cart_id>/", CartDetailAPIView.as_view(), name="cart-detail"),

    # Order URLs
    path("orders/", OrderCreateAPIView.as_view(), name="order-create"),

    # Blog URLs
    path("blogs/", BlogListAPIView.as_view(), name="blog-list"),
    path("blogs/<uuid:blog_id>/", BlogDetailAPIView.as_view(), name="blog-detail"),
]
