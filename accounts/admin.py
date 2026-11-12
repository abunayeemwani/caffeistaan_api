from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', 'is_cafe_staff', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_cafe_staff', 'is_staff', 'is_active')
    search_fields = ('phone', 'full_name')
    ordering = ('-date_joined',)