from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.


# shopping cart model:

class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, related_name="shopping_cart", on_delete=models.CASCADE)
    # payments=models.ManyToOneRel(related_name="shopping_cart",on_delete=models.RESTRICT)

    class Meta:
        db_table = "ShoppingCart"
        ordering = ["user"]
        verbose_name = "ShoppingCart"
        verbose_name_plural = "ShoppingCarts"


# cart item model:


def get_unknown_product():
    product = Product.objects.get_or_create(name="nonexistent product",
                                            description="This product is no longer available.",
                                            balance=0, price=0, category=None)
    return product


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, related_name="cart_item", on_delete=models.SET(get_unknown_product))
    shopping_cart = models.ForeignKey(
        ShoppingCart, related_name="cart_items", on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CartItem"
        ordering = ["date"]
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"

    def total(self):
        return self.number * self.product.price

    def __str__(self):
        return f"{self.number}x {self.product.name}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET(get_unknown_product),
        null=True,
        blank=True,
        related_name="order_items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    number = models.PositiveIntegerField(default=1)
    price = models.BigIntegerField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "OrderItem"
        ordering = ["date"]
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return f"{self.number} × {self.name}"

    def save(self, *args, **kwargs):
        if self.product:
            if not self.name:
                self.name = self.product.name
            if not self.description:
                self.description = self.product.description
            if not self.category and self.product.category:
                self.category = str(self.product.category)
            if not self.price:
                self.price = self.product.price
        super().save(*args, **kwargs)
