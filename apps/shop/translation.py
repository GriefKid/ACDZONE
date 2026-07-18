from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description')
