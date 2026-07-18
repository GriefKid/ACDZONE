from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin

from apps.core.translations import translate_lazy as _

from .models import Post


@admin.register(Post)
class PostAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('title', 'channel', 'category', 'is_urgent', 'is_active', 'published_at')
    list_editable = ('is_urgent', 'is_active')
    list_filter = ('channel', 'category', 'is_urgent', 'is_active')
    search_fields = ('title', 'summary', 'body', 'tags', 'source_name')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': (('channel', 'is_urgent', 'is_active'), 'published_at', 'slug')}),
        (_('محتوا'), {'fields': ('title', 'summary', 'body', 'image', 'image_url')}),
        (_('فقط ACDNews'), {
            'fields': ('category', 'tags', 'source_name', 'source_url'),
            'description': (
                'دسته‌بندی به‌صورت خودکار هم از روی تگ‌ها تشخیص داده می‌شود — اگر یکی از '
                'این چهار کلمه را به‌عنوان یک تگ اضافه کنید (ورزشی، اقتصادی، سیاسی، '
                'اجتماعی)، همان‌جا از لیست تگ‌ها حذف و به‌جایش به‌عنوان دسته ثبت می‌شود.'
            ),
        }),
        (_('زمان'), {'fields': ('created_at',)}),
    )
