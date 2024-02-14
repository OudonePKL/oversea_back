from django.contrib import admin
from .models import Category, Product, Review, Order, OrderItem, Payment, Cart, CartItem, ProductImage, Size, Color

# Register your models here

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(Color)
