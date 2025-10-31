from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.


# shopping cart model:

class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, related_name="shopping_cart", on_delete=models.CASCADE)
    # payments=models.ManyToOneRel(related_name="shopping_cart",on_delete=models.RESTRICT)

# cart item model:


def get_unknown_product():
    product = Product.objects.get_or_create(name="nonexistent product",
                                            description="This product is no longer available.",
                                            balance=0, price=0, category=None)
    return product


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, related_name="cart_item", on_delete=models.SET(get_unknown_product))
    shopping_cart = models.ForeignKey(ShoppingCart,related_name="cart_items",on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    def total(self):
        return self.number * self.product.price

    def __str__(self):
        return f"{self.number}x {self.product.name}"