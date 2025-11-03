from django.contrib import admin
from .models import Product, Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("tage_name", "products")
    list_filter = ("tage_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "balance",
                    "price", "public_id", "category")
    list_filter = ("name", "price")
    search_fields = ("name", "price", "category")
