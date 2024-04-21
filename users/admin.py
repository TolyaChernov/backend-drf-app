from django.contrib import admin

from .models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_admin")
