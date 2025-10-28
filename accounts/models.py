from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    def __str__(self):
        return self.first_name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE)
    #orders
    #profile
    def __str__(self):
        return self.email

