from django.urls import path

from apps.ecommerce.api.cart import CartDetailAPIView
from apps.ecommerce.api.product import (
    ProductListAPIView,
    ProductDetailAPIView, 
    CategoryListAPIView
)
from apps.ecommerce.api.order import OrderCreateAPIView

urlpatterns = [
    # Product URLs
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<uuid:product_id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    
    # Cart URLs
    path('carts/<uuid:cart_id>/', CartDetailAPIView.as_view(), name='cart-detail'),
    
    # Order URLs
    path('orders/', OrderCreateAPIView.as_view(), name='order-create'),
] 