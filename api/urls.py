from django.urls import path
from .views import (
    ProductListAPIView, CreateProductAPIView, UpdateProductAPIView, DeleteProductAPIView, ProductDetailAPIView,
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    CartListView, CartDetailView, CreateCartView, UserCartListView, CartDeleteView,
    OrderListView, OrderDetailView, UserOrderListView, OrderDeleteView,
    ReviewListCreate, ReviewRetrieveUpdateDestroy, UserReviewListView, ReviewDeleteView,
    PaymentListCreate, PaymentRetrieveUpdateDestroy, UserPaymentListView, PaymentDeleteView
)

urlpatterns = [
    # Category
    path('categories', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>', CategoryRetrieveUpdateDestroy.as_view(), name='category-retrieve-update-destroy'),
    # Product
    path('products/create', CreateProductAPIView.as_view(), name='create-product'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/update/<int:pk>', UpdateProductAPIView.as_view(), name='update-product'),
    path('products/delete/<int:pk>', DeleteProductAPIView.as_view(), name='delete-product'),
    # Cart
    path('carts', CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>', CartDetailView.as_view(), name='cart-detail'),
    path('user/<int:user_id>/carts', UserCartListView.as_view(), name='user-cart-list'),
    path('create-cart', CreateCartView.as_view(), name='create_cart'),
    path('carts/delete/<int:pk>', CartDeleteView.as_view(), name='delete-cart'),
    # Order
    path('orders', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('user/<int:user_id>/orders', UserOrderListView.as_view(), name='user-order-list'),
    path('orders/delete/<int:pk>', OrderDeleteView.as_view(), name='delete-order'),
    # Review
    path('reviews', ReviewListCreate.as_view(), name='review-list-create'),
    path('reviews/<int:pk>', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),
    path('user/<int:user_id>/reviews', UserReviewListView.as_view(), name='user-reviews-list'),
    path('reviews/delete/<int:pk>', ReviewDeleteView.as_view(), name='delete-reviews'),
    # Payment
    path('payments', PaymentListCreate.as_view(), name='payments-list-create'),
    path('payments/<int:pk>', PaymentRetrieveUpdateDestroy.as_view(), name='payments-detail'),
    path('user/<int:user_id>/payments', UserPaymentListView.as_view(), name='user-payments-list'),
    path('payments/delete/<int:pk>', PaymentDeleteView.as_view(), name='delete-payments'),
]


