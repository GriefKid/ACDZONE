from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin

from apps.core.translations import translate_lazy as _

from .models import Category, Order, Product


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('name', 'page', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('page', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'page')}),
        (_('نمایش'), {'fields': (('order', 'is_active'),)}),
    )


@admin.register(Product)
class ProductAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_active', 'order')
    list_editable = ('price', 'is_active', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'long_description')
    fieldsets = (
        (None, {'fields': ('category', 'title')}),
        (_('محتوا'), {'fields': ('description', 'long_description')}),
        (_('رسانه'), {'fields': ('image', 'image_url')}),
        (_('قیمت و نمایش'), {'fields': (('price', 'is_active', 'order'),)}),
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """`stage` is editable right from the list view on purpose: the real
    ACDPay/ACDBallons sales process is manual and human-in-the-loop (over
    WhatsApp/Telegram/Bale), so the site owner updates an order's stage
    here as the conversation with the customer progresses — no separate
    workflow tool needed."""

    list_display = ('id', 'product', 'user', 'stage', 'contact_number', 'created_at')
    list_editable = ('stage',)
    list_filter = ('stage', 'product__category')
    search_fields = ('full_name', 'contact_number', 'email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'product', 'stage')}),
        (_('اطلاعات مشتری'), {'fields': (('full_name', 'contact_number'), 'email')}),
        (_('داخلی'), {'fields': ('admin_note', 'is_hidden')}),
        (_('زمان'), {'fields': (('created_at', 'updated_at'),)}),
    )
