from django.db import models




# Create your models here.


class Category(models.Model):
    tag_name = models.CharField(blank=False, max_length=30)

    class Meta:
        db_table = "Category"
        ordering = ["tag_name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=False)
    balance = models.IntegerField()
    price = models.BigIntegerField()
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.RESTRICT)



    class Meta:
        db_table = "Product"
        ordering = ["price", "name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
