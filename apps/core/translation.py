from modeltranslation.translator import TranslationOptions, register

from .models import Attraction, Country, Hotel, Representative, TravelRoute


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = (
        'name', 'description', 'capital', 'official_language', 'currency', 'best_time_to_visit',
        'weather_spring', 'weather_summer', 'weather_autumn', 'weather_winter',
    )


@register(Representative)
class RepresentativeTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'position', 'bio')


@register(Attraction)
class AttractionTranslationOptions(TranslationOptions):
    fields = ('name', 'summary', 'description')


@register(TravelRoute)
class TravelRouteTranslationOptions(TranslationOptions):
    fields = ('duration_text', 'notes')


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name', 'city', 'address', 'summary', 'description')
