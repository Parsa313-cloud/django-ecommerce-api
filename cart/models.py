import uuid
from decimal import Decimal
from django.db import models
from accounts.models import User
from products.models import Product


class ShoppingCart(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User,
        related_name="shopping_cart",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "ShoppingCart"
        ordering = ["user"]
        verbose_name = "ShoppingCart"
        verbose_name_plural = "ShoppingCarts"

    def __str__(self):
        return f"Cart of {self.user.email}"


def get_unknown_product():
    product, _ = Product.objects.get_or_create(
        name="Nonexistent Product",
        defaults={
            "description": "This product is no longer available.",
            "balance": 0,
            "price": Decimal("0.00"),
            "category": "Unknown",
        },
    )
    return product


class CartItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    product = models.ForeignKey(
        Product,
        related_name="cart_items",
        on_delete=models.SET(get_unknown_product),
    )
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        related_name="cart_items",
        on_delete=models.CASCADE,
    )
    number = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CartItem"
        ordering = ["date"]
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"

    @property
    def total(self):

        return self.number * self.product.price

    def __str__(self):
        return f"{self.number} × {self.product.name}"


class OrderItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        User,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.SET(get_unknown_product),
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    number = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "OrderItem"
        ordering = ["-time"]
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
            if not self.category and getattr(self.product, "category", None):
                self.category = str(self.product.category)
                if self.price is None:
                    self.price = self.product.price
        super().save(*args, **kwargs)
