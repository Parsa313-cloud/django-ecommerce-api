from django.contrib import admin
from .models import ShoppingCart, CartItem, OrderItem
from django import forms


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
    list_display = ['product', 'get_user_email', 'number', 'total']
    search_fields = ["public_id", 'product__name', 'shopping_cart__user__email']

    def get_user_email(self, obj):
        return obj.shopping_cart.user.email
    get_user_email.short_description = "User Email"


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["description"].required = False
        self.fields["category"].required = False
        self.fields["price"].required = False

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemAdminForm
    list_display = ("name", "user", "number", "price", "time")
    list_filter = ("user", "time")
    search_fields = ("product__name", "user__email")
