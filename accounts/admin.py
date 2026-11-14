from django.contrib import admin
from .models import User
from .models import CustomerProfile, Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', 'is_cafe_staff', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_cafe_staff', 'is_staff', 'is_active')
    search_fields = ('phone', 'full_name')
    ordering = ('-date_joined',)




class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    fields = ('address_label', 'recipient_name', 'phone', 'street_address', 'locality', 'postal_code', 'is_default')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'loyalty_points', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_label', 'recipient_name', 'phone', 'locality', 'is_default', 'user')
    list_filter = ('address_label', 'is_default')
    search_fields = ('recipient_name', 'phone', 'street_address', 'locality', 'user__username')