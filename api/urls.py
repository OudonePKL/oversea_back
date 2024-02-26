from django.urls import path
from .views import (
    ProductListAPIView, CreateProductAPIView, UpdateProductAPIView, DeleteProductAPIView, ProductDetailAPIView,
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    CartListView, CartDetailView, UserCartListView, CartDeleteView, CartCreateAPIView, CartUpdateAPIView,
    SearchView, OrderListView, OrderDetailView, UserOrderListView, OrderDeleteView, OrderCreateAPIView, OrderUpdateAPIView ,
    ReviewListCreate, ReviewRetrieveUpdateDestroy, UserReviewListView, ReviewDeleteView,ProductReviewListView,
    PaymentListCreate, PaymentRetrieveUpdateDestroy, UserPaymentAPIView,
    CreateOrderView
)

urlpatterns = [
    # Category
    path('categories', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<int:pk>', CategoryRetrieveUpdateDestroy.as_view(), name='category-retrieve-update-destroy'),
    # Product
    path("", ProductListAPIView.as_view(), name="product-list-by-category"),  # Product list related
    path('product/create', CreateProductAPIView.as_view(), name='create-product'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:id>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product/update/<int:pk>', UpdateProductAPIView.as_view(), name='update-product'),
    path('product/delete/<int:pk>', DeleteProductAPIView.as_view(), name='delete-product'),
    # Cart
    path('carts', CartListView.as_view(), name='cart-list'),
    path('cart/<int:pk>', CartDetailView.as_view(), name='cart-detail'),
    path('user/<int:user_id>/cart', UserCartListView.as_view(), name='user-cart-list'),
    path('cart/create', CartCreateAPIView.as_view(), name='create_cart'),
    path('cart/update/<int:pk>', CartUpdateAPIView.as_view(), name='cart-update'),
    path('cart/delete/<int:pk>', CartDeleteView.as_view(), name='delete-cart'),
    # Order
    path("search", SearchView.as_view(), name="search"),  # Order related
    path('orders', OrderListView.as_view(), name='order-list'),

    path('create-order', CreateOrderView.as_view(), name='create-order'),
    path('order/create', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/update/<int:pk>', OrderUpdateAPIView.as_view(), name='order-update'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('user/<int:user_id>/order', UserOrderListView.as_view(), name='user-order-list'),
    path('order/delete/<int:pk>', OrderDeleteView.as_view(), name='delete-order'),
    # Review
    path('reviews', ReviewListCreate.as_view(), name='review-list-create'),
    path('review/<int:pk>', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),
    path('review/update/<int:pk>', ReviewRetrieveUpdateDestroy.as_view(), name='review-update'),
    path('user/<int:user_id>/review', UserReviewListView.as_view(), name='user-reviews-list'),
    path('product/<int:product_id>/review', ProductReviewListView.as_view(), name='product-reviews-list'),
    path('review/delete/<int:pk>', ReviewDeleteView.as_view(), name='delete-reviews'),
    # Payment
    path('payments', PaymentListCreate.as_view(), name='payments-list-create'),
    path('payment/<int:pk>', PaymentRetrieveUpdateDestroy.as_view(), name='payments-detail'),
    path('user/<int:user_id>/payment', UserPaymentAPIView.as_view(), name='user-payments')
]


