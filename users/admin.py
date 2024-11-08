from django.contrib import admin

from .models import CustomsUser


@admin.register(CustomsUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "avatar", "phone_number")
    list_filter = ("phone_number",)
    search_fields = ("email",)
