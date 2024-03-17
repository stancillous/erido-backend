from django.contrib import admin
from .models import User, Category, Product, ShoppingCart, CartItem, Order, OrderItem, Review, Address, Payment

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'auth0_user_id')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'description', 'price', 'quantity_in_stock', 'category',)

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'cart', 'product', 'quantity',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'order_status', 'created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'quantity', 'unit_price',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'product', 'user', 'rating', 'comment', 'created_at',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'user', 'street_address', 'town', 'zipcode', 'county', 'phone_number_1', 'phone_number_2',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'amount', 'payment_status', 'payment_method', 'transaction_id', 'created_at',)
