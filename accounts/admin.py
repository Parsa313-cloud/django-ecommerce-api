from django.contrib import admin
from .models import User, Profile

# Register your models here.


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]
    inlines = [ProfileInline]
    search_fields = ['username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "address",
                    "phone_number", "slug", "created_at", "updated_at"]
    search_fields = ["first_name", "last_name", "slug"]
