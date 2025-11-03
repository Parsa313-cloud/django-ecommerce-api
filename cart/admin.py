from django.contrib import admin
from .models import ShoppingCart, CartItem, OrderItem
from products.models import Product
# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [CartItemInline]


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    can_delete = False


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['number', "public_id", "date", "shopping_cart"]
    inlines = [ProductInline]
    search_fields = ["public_id", "date"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description",
                    "category", "number", "price", "time"]
    inlines = [Product]
