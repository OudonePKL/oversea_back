from rest_framework import serializers
from .models import Category, Product, Size, Color, ProductImage, Cart, CartItem, Order, OrderItem, Review, Payment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_sizes(self, obj):
        sizes = Size.objects.filter(product=obj)
        serializer = SizeSerializer(sizes, many=True)
        return serializer.data
    
    def get_colors(self, obj):
        colors = Color.objects.filter(product=obj)
        serializer = ColorSerializer(colors, many=True)
        return serializer.data
    
    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj)
        serializer = ProductImageSerializer(images, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = '__all__'

class CreateProductSerializer(serializers.ModelSerializer):
    sizes = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True)
    colors = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True)
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'created_by', 'sizes', 'colors', 'images']

    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes', [])
        colors_data = validated_data.pop('colors', [])
        images_data = validated_data.pop('images', [])

        product = Product.objects.create(**validated_data)

        for size_name in sizes_data:
            Size.objects.create(product_id=product.id, name=size_name)

        for color_name in colors_data:
            Color.objects.create(product_id=product.id, name=color_name)

        for image_file in images_data:
            ProductImage.objects.create(product_id=product.id, image=image_file)

        return product
    
class UpdateProductSerializer(serializers.ModelSerializer):
    sizes = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    colors = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'created_by', 'sizes', 'colors', 'images']

    def update(self, instance, validated_data):
        sizes_data = validated_data.pop('sizes', None)
        colors_data = validated_data.pop('colors', None)
        images_data = validated_data.pop('images', None)

        # Update the Product instance
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()

        # Update related Size instances
        if sizes_data is not None:
            Size.objects.filter(product=instance).delete()
            for size_name in sizes_data:
                Size.objects.create(product=instance, name=size_name)

        # Update related Color instances
        if colors_data is not None:
            Color.objects.filter(product=instance).delete()
            for color_name in colors_data:
                Color.objects.create(product=instance, name=color_name)

        # Update related ProductImage instances
        if images_data is not None:
            ProductImage.objects.filter(product=instance).delete()
            for image_file in images_data:
                ProductImage.objects.create(product=instance, image=image_file)

        return instance

# Cart
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'color', 'size']

class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        serializer = CartItemSerializer(cart_items, many=True)
        return serializer.data

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user']

    def create(self, validated_data):
        cart = Cart.objects.create(user=validated_data['user'])
        return cart

# Order
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'color', 'size']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'items']


# =========== Create order not yet ===========
# Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'





