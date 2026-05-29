from django.contrib import admin
from .models import HomePage, PartnerLogo, FeatureCard, FAQ


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1


class FeatureCardInline(admin.TabularInline):
    model = FeatureCard
    extra = 1


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    inlines = [PartnerLogoInline, FeatureCardInline, FAQInline]

    # اجازه نده بیشتر از یک HomePage ساخته شود
    def has_add_permission(self, request):
        if HomePage.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    search_fields = ("title",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)
    search_fields = ("question",)
