import uuid

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class Category(models.Model):
    tag_name = models.CharField(
        blank=False, max_length=30, unique=True, db_index=True,)

    class Meta:
        db_table = "Category"
        ordering = ["tag_name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tag_name


class Product(models.Model):
    name = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=False)
    balance = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    public_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.RESTRICT)

    class Meta:
        db_table = "Product"
        ordering = ["price", "name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.category.tag_name})"

    def clean(self):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
