from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.


# shoping cart model:

class Shoping_cart(models.Model):
    user = models.ForeignKey(
        User, related_name="shoping_cart", on_delete=models.CASCADE)
    # payments=models.ManyToOneRel(related_name="shoping_cart",on_delete=models.RESTRICT)

# cart item model:


def get_unkown_product():
    product = Product.objects.get_or_create(name="nonexistent product",
                                            description="This product is no longer available.",
                                            balance=0, price=0, category=None)
    return product


class Cart_Item(models.Model):
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.SET(get_unkown_product()))
    # shoping_cart=models.ForeignKey(,related_name="cart_items",on_delete=models.CASCADE)
    number = models.IntegerField()
    total = models.BigIntegerField()
    date = models.DateTimeField()
