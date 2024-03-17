from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_dict(self, request=None):
        return {
            'category_id': self.category_id,
            'name': self.name,
        }

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.PositiveIntegerField(null=False)
    quantity_in_stock = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='images', null=False, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def to_dict(self, request=None):
        image_url = self.image.url

        if request and image_url:
            image_url = request.build_absolute_uri(image_url)

        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'quantity_in_stock': self.quantity_in_stock,
            'category': self.category.to_dict() if self.category else None,
            'image': image_url
        }

class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart ID: {self.cart_id} - User: {self.user}'

    def to_dict(self, request=None):
        return {
            'cart_id': self.cart_id,
            'user': self.user.username,
            'created_at': str(self.created_at),
        }

class CartItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Item ID: {self.item_id} - Product: {self.product.name} - Quantity: {self.quantity}'

    def to_dict(self, request=None):
        return {
            'item_id': self.item_id,
            'cart': self.cart.to_dict() if self.cart else None,
            'product': self.product.to_dict() if self.product else None,
            'subtotal': self.product.price * self.quantity,
            'quantity': self.quantity,
        }

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order ID: {self.order_id} - User: {self.user.username} - Status: {self.order_status}'

    def to_dict(self, request=None):
        return {
            'order_id': self.order_id,
            'user': self.user.id,
            'total_amount': str(self.total_amount),
            'order_status': self.order_status,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return f'Review ID: {self.review_id} - Product: {self.product.name} - User: {self.user.username}'

    def to_dict(self, request=None):
        return {
            'order_item_id': self.item_id,
            'order': self.order.order_id, # Assuming you want to include the order ID
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review ID: {self.review_id} - Product: {self.product.name} - User: {self.user.username}'

    def to_dict(self, request=None):
        return {
            'review_id': self.review_id,
            'product': self.product.to_dict() if self.product else None,
            'user': self.user.username,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    county = models.CharField(max_length=255, null=True)
    phone_number_1 = models.CharField(max_length=255, null=True)
    phone_number_2 = models.CharField(max_length=255, null=True)
    additional_details = models.TextField(null=True)


    def __str__(self):
        return f'Address ID: {self.address_id} - User: {self.user.username}'

    def to_dict(self, request=None):
        return {
            'address_id': self.address_id,
            'user': self.user.id,
            'street_address': self.street_address,
            'town': self.town,
            'zipcode': self.zipcode,
            'county': self.county,
            'phone_number_1': self.phone_number_1,
            'phone_number_2': self.phone_number_2,
        }

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment ID: {self.payment_id} - Order: {self.order.order_id} - Status: {self.payment_status}'

    def to_dict(self, request=None):
        return {
            'payment_id': self.payment_id,
            'order': self.order.to_dict() if self.order else None,
            'amount': str(self.amount),
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'created_at': str(self.created_at),
        }
