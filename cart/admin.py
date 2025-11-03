from django.contrib import admin
from .models import ShoppingCart, CartItem, OrderItem
from products.models import Product
# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ['total']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'shopping_cart', 'number', 'total', 'date']
    search_fields = ["public_id", 'product__name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["name","product",
                    "category","number", "price", "time"]
    search_fields = ['name', 'product__name', 'user__email']
    list_filter = ['category', 'time']

