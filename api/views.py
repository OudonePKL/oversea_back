import base64
import uuid
from collections import Counter
from pprint import pprint
from PIL import Image
import io
import django
from django.core.files.base import ContentFile
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission


from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Color, Size, ProductImage, Cart, CartItem, Order, OrderItem, Review, Payment
from .serializers import (
    ProductListSerializer, CreateProductSerializer, UpdateProductSerializer,
    CategorySerializer,
    CartSerializer, CreateCartSerializer, CartUpdateSerializer,
    OrderSerializer, OrderCreateSerializer, OrderCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer,
    PaymentSerializer, UserPaymentSerializer
    )
from .permissions import IsOwnerOrReadOnly


class CategoryListCreate(generics.ListCreateAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Get the original queryset
        queryset = Category.objects.all()
        # Exclude specific data, for example, 'Food'
        queryset = queryset.exclude(name='Food')
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response({"message": "success"}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({"message": "success"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"message": "success"}, status=status.HTTP_200_OK)


# class ProductListAPIView(generics.ListAPIView):
#     def get(self, request, goods_id=None):
#         """
#          <View product>
#          goods_id O -> View details
#          goods_id
#          * Separately removed due to merchant permission issues *
#          """
#         if goods_id is None:
#             category = request.GET.get('category', '1')  # You can provide default values.
#             goods = Product.objects.all()
#             if not goods.exists():
#                 return Response([], status=200)
#             """
#              <Filtering branch>
#              - Latest
#              - Old shoots
#              - Price ascending & descending order
#              - Ascending & descending number of reviews (5,6)
#              """
#             if category == '2':
#                 goods = goods.order_by(
#                     "-price"
#                 )
#             elif category == '3':
#                 goods = goods.annotate(review_count=Count("reviewmodel")).order_by(
#                     "-review_count"
#                 )
#             elif category == '4':
#                 goods = goods.order_by(
#                     "price"
#                 )
#             elif category == '5':
#                 goods = goods.annotate(order_count=Count("ordermodel")).order_by(
#                     "-order_count"
#                 )
#             elif category == '6':
#                 goods = goods.annotate(order_count=Count("ordermodel")).order_by(
#                     "-created_at"
#                 )
#             else:
#                 try:
#                     goods = goods.order_by("-price")
#                 except Exception as e:
#                     print(e)
#                     return Response(
#                         {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
#                     )
#             serializer = ProductListSerializer(goods, many=True)
#             return Response(serializer.data, status=200)
#         else:
#             goods = get_object_or_404(Product, id=goods_id)
#             serializer = ProductListSerializer(goods)
#             order_total = Order.objects.filter(user_id=request.user.id, goods=goods).count()
#             review_total = Review.objects.filter(user_id=request.user.id, goods=goods).count()
#             result = serializer.data.copy()
#             if order_total >= review_total:
#                 result['is_ordered'] = True
#             else:
#                 result['is_ordered'] = False
#             return Response(result, status=200)
    

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', '1')  # You can provide default values.
        goods = Product.objects.all()
        
        if category == '2':
            goods = goods.order_by("-price")
        elif category == '3':
            goods = goods.annotate(review_count=Count("review")).order_by("-review_count")
        elif category == '4':
            goods = goods.order_by("price")
        else:
            goods = goods.order_by("-created_at")
        
        return goods

    def get(self, request, goods_id=None):
        """
        <View product>
        goods_id O -> View details
        goods_id
        * Separately removed due to merchant permission issues *
        """
        if goods_id is None:
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response([], status=200)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            goods = get_object_or_404(Product, id=goods_id)
            serializer = self.serializer_class(goods)
            order_total = Order.objects.filter(user_id=request.user.id, goods=goods).count()
            review_total = Review.objects.filter(user_id=request.user.id, goods=goods).count()
            result = serializer.data.copy()
            if order_total >= review_total:
                result['is_ordered'] = True
            else:
                result['is_ordered'] = False
            return Response(result, status=200)
        

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateProductAPIView(APIView):
    def post(self, request, format=None):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({"message": "success"},status=status.HTTP_201_CREATED)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProductAPIView(APIView):
    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductAPIView(APIView):
    def delete(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete related Size instances
        Size.objects.filter(product=product).delete()

        # Delete related Color instances
        Color.objects.filter(product=product).delete()

        # Delete related ProductImage instances
        ProductImage.objects.filter(product=product).delete()

        # Delete the Product instance
        product.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)

# Cart
class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class UserCartListView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Cart.objects.filter(user_id=user_id)

class CartCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartUpdateSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDeleteView(generics.DestroyAPIView):
    def delete(self, request, pk, format=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete related CartItem instances
        CartItem.objects.filter(cart_id=cart).delete()

        # Delete the Cart instance
        cart.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)

class CartItemDeleteView(generics.DestroyAPIView):
    def delete(self, request, pk, format=None):
        try:
            cartItme = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the Cart instance
        cartItme.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)

# Order
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Retrieve orders with status "Pending"
        return Order.objects.filter(status="Pending")

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)
    

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderCreateSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderDeleteView(generics.DestroyAPIView):
    def delete(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete related OrderItem instances
        OrderItem.objects.filter(order_id=order).delete()

        # Delete the Order instance
        order.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)

# Review
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(user_id=user_id)

class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

class ReviewDeleteView(generics.DestroyAPIView):
    def delete(self, request, pk, format=None):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        
        review.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)

# Payment
class PaymentListCreate(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class UserPaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(user_id=user_id)

class UserPaymentAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = UserPaymentSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']  # Assuming user_id is passed in the URL
        return self.get_queryset().filter(user_id=user_id).first()


class SearchView(APIView):
    # @swagger_auto_schema(
    #     tags=["search"], request_body=PostSerializer, responses={200: "Success"}
    # )
    def post(self, request):
        search_word = request.data.get("search")
        product_set = Product.objects.filter(
            Q(name__icontains=search_word)
        )

        products = ProductListSerializer(product_set, many=True).data

        return Response(products, status=status.HTTP_200_OK)