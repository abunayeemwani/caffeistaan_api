from django.contrib import admin
from .models import MenuCategory, Dish, DishImage, DishVariant, AddOn


class DishImageInline(admin.TabularInline):
    model = DishImage
    extra = 1


class DishVariantInline(admin.TabularInline):
    model = DishVariant
    extra = 1


class AddOnInline(admin.TabularInline):
    model = AddOn
    extra = 1


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'discounted_price', 'dietary_type', 'is_available', 'is_featured')
    list_filter = ('category', 'dietary_type', 'is_available', 'is_featured')
    list_editable = ('is_available', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DishImageInline, DishVariantInline, AddOnInline]