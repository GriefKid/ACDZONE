from django import template
from django.urls import NoReverseMatch, reverse
from django.utils import translation

from apps.core.translations import translate

register = template.Library()


@register.simple_tag
def t(persian_text):
    """{% t "متن فارسی" %} — drop-in replacement for {% trans %} that
    doesn't need compiled .mo files (see apps/core/translations.py for
    why). Works with literal strings and template variables alike:

        {% t "به ACD Zone خوش آمدید" %}
        {% t product.title %}
    """
    return translate(persian_text)


@register.simple_tag(takes_context=True)
def language_url(context, lang_code):
    """Returns the URL of the page being viewed right now, re-resolved in
    `lang_code`. Used by the header's language switcher.

    Reverses using the resolved view name plus its actual positional/
    keyword arguments (request.resolver_match.args/kwargs), so this works
    for every view — including ones that take URL parameters, like the
    buy page — not just parameterless ones. That's also what avoids
    depending on Django's automatic translate_url/next-URL rewriting,
    which wasn't reliably dropping the English prefix when switching back
    to the default language.
    """
    request = context.get('request')
    match = getattr(request, 'resolver_match', None)
    if match is None:
        return '/'
    with translation.override(lang_code):
        try:
            return reverse(match.view_name, args=match.args, kwargs=match.kwargs)
        except NoReverseMatch:
            return '/'
