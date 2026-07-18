from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin

from apps.core.translations import translate_lazy as _

from .models import Attraction, Country, Hotel, Notification, Representative, TravelRoute


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    """Read-mostly — these are only ever created by Order.save() /
    Post.save(), never written by hand. Registered so the site owner can
    audit what actually went out to a user, not as a data-entry screen."""

    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('user', 'message', 'link', 'created_at')
    fieldsets = (
        (None, {'fields': (('user', 'is_read'), 'message', 'link', 'created_at')}),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Country)
class CountryAdmin(TranslationAdmin, ModelAdmin):
    """Fully admin-managed list behind the header's "کشورها" dropdown —
    add, translate, reorder, or deactivate a country here; slug is
    generated automatically from the name (see Country.save()) unless you
    type your own."""

    list_display = ('name', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name_fa', 'name_en', 'slug')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': (('is_active', 'order'), 'name', 'slug')}),
        (_('کشور در یک نگاه'), {
            'fields': (('capital', 'official_language'), ('currency', 'calling_code'), 'best_time_to_visit'),
        }),
        (_('پرچم'), {'fields': ('flag_image', 'flag_image_url')}),
        (_('تصویر پس‌زمینه'), {'fields': ('background_image', 'background_image_url')}),
        (_('سرود ملی'), {'fields': ('anthem_audio', 'anthem_audio_url')}),
        (_('توضیحات'), {'fields': ('description',)}),
        (_('آب‌وهوا در فصل‌های مختلف'), {
            'fields': ('weather_spring', 'weather_summer', 'weather_autumn', 'weather_winter'),
        }),
        (_('زمان'), {'fields': ('created_at',)}),
    )


@admin.register(Representative)
class RepresentativeAdmin(TranslationAdmin, ModelAdmin):
    """Admin-managed entries behind the header's "نماینده‌ها" dropdown."""

    list_display = ('full_name', 'country', 'phone', 'email', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'country')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'country__name_fa', 'country__name_en')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('country',)
    fieldsets = (
        (None, {'fields': (('is_active', 'order'), ('first_name', 'last_name'), 'slug', 'country', 'position')}),
        (_('عکس نماینده'), {'fields': ('photo', 'photo_url')}),
        (_('اطلاعات تماس'), {'fields': ('phone', 'email')}),
        (_('توضیحات'), {'fields': ('bio',)}),
        (_('زمان'), {'fields': ('created_at',)}),
    )


@admin.register(Attraction)
class AttractionAdmin(TranslationAdmin, ModelAdmin):
    """One card in a Country page's "جاذبه‌های گردشگری" section — add as
    many per country as you want; slug is auto-generated from the name
    (see Attraction.save()) unless you type your own."""

    list_display = ('name', 'country', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'country')
    search_fields = ('name_fa', 'name_en', 'country__name_fa', 'country__name_en')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('country',)
    fieldsets = (
        (None, {'fields': (('is_active', 'order'), 'country', 'name', 'slug', 'summary')}),
        (_('عکس'), {'fields': ('image', 'image_url')}),
        (_('توضیحات کامل'), {'fields': ('description',)}),
        (_('زمان'), {'fields': ('created_at',)}),
    )


@admin.register(Hotel)
class HotelAdmin(TranslationAdmin, ModelAdmin):
    """One card in a Country page's "هتل‌های معروف" section — add as many
    per country as you want. booking_url is optional; when set, the
    hotel's card on the site links out to it."""

    list_display = ('name', 'country', 'city', 'star_rating', 'phone_number', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'star_rating', 'country')
    search_fields = ('name_fa', 'name_en', 'city_fa', 'city_en', 'country__name_fa', 'country__name_en')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('country',)
    fieldsets = (
        (None, {'fields': (('is_active', 'order'), 'country', 'name', 'slug', ('city', 'star_rating'), 'summary')}),
        (_('عکس'), {'fields': ('image', 'image_url')}),
        (_('اطلاعات تماس'), {'fields': ('address', 'phone_number')}),
        (_('توضیحات کامل'), {'fields': ('description',)}),
        (_('قیمت'), {'fields': ('price_usd',)}),
        (_('لینک رزرو'), {'fields': ('booking_url',)}),
        (_('زمان'), {'fields': ('created_at',)}),
    )


@admin.register(TravelRoute)
class TravelRouteAdmin(TranslationAdmin, ModelAdmin):
    """One row of the "از کجا تا اینجا چقدر راهه؟" calculator on a
    destination country's page. See TravelRoute's own docstring in
    models.py for why nothing here is auto-computed — every row is a
    real, deliberately-entered distance/duration."""

    list_display = ('origin_country', 'destination_country', 'mode', 'distance_km', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'mode', 'destination_country')
    search_fields = (
        'origin_country__name_fa', 'origin_country__name_en',
        'destination_country__name_fa', 'destination_country__name_en',
    )
    autocomplete_fields = ('origin_country', 'destination_country')
    fieldsets = (
        (None, {'fields': ('is_active', ('origin_country', 'destination_country'), 'mode')}),
        (_('فاصله و زمان'), {'fields': ('distance_km', 'duration_text')}),
        (_('توضیحات اضافه'), {'fields': ('notes',)}),
    )
