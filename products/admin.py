from django.contrib import admin
from .models import Product, Category

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("tag_name", "show_products")
    list_filter = ("tag_name",)
    inlines = [ProductInline]

    def show_products(self, obj):
        products = obj.products.all()
        if not products:
            return "—"

        return ", ".join([p.name for p in products])

    show_products.short_description = "Products"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","balance",
                    "price", "public_id", "category")
    list_filter = ("name", "price")
    search_fields = ("name", "price", "category__tag_name")
