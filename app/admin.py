from django.contrib import admin
from app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

