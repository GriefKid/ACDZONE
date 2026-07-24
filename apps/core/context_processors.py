from django.middleware.csrf import get_token
from apps.core.vpn_detection import get_vpn_status

# Safe to import at module level (unlike ChatMessage's local import below) —
# Country lives in this exact same app (apps.core.models), so there's no
# cross-app loading-order question to worry about.
from apps.core.models import Country, Representative


def site_settings(request):
    """
    Site-wide values available in every template (used by the shared header
    and footer partials).

    These are hard-coded placeholders for now. Once the SiteSettings model
    exists (next stage), this will read from the database instead so the
    admin can change the site name, logo, and social links without a
    code deploy.
    """
    context = {
        'SITE_NAME': 'ACD Zone',
        'CONTACT_TELEGRAM_URL': '#',
        'CONTACT_WHATSAPP_URL': '#',
        'vpn_status': get_vpn_status(request),
    }

    # The floating chat widget (templates/partials/chat_widget.html) sends
    # its messages via fetch() with an X-CSRFToken header read straight
    # from the csrftoken cookie — but Django only actually sets that
    # cookie on the response once something calls get_token() during the
    # request. Plenty of pages the widget appears on (the home page, a
    # blog listing, ...) don't render any {% csrf_token %} form tag, so
    # without this the cookie might simply not exist yet the first time
    # someone tries to send a chat message. This context processor runs
    # on every single page, so calling it here guarantees the cookie is
    # always present before the widget's JS ever needs it.
    get_token(request)

    # The header's country dropdown (templates/partials/header.html) is
    # shown to every visitor, logged in or not — Country.Meta.ordering
    # (['order', 'id']) already sorts this correctly with no extra
    # .order_by() needed.
    context['countries'] = Country.objects.filter(is_active=True)
    context['representatives'] = (
        Representative.objects.filter(is_active=True, country__is_active=True)
        .select_related('country')
    )

    # The notification bell lives in the header, so every page needs these
    # two — cheap enough (one small slice + one count query) to always run
    # for logged-in requests rather than wiring a per-view context dict.
    if request.user.is_authenticated:
        context['recent_notifications'] = request.user.notifications.all()[:8]
        context['unread_notifications_count'] = request.user.notifications.filter(is_read=False).count()

        # Local import: apps.support.models imports apps.core.models
        # (Notification), so importing apps.support at the top of this
        # module would run at Django-app-loading time — this file is only
        # ever imported later, lazily, by the template engine on first
        # use, well after the app registry is ready, but keeping the
        # import local here avoids relying on that ordering at all.
        from apps.support.models import ChatMessage
        context['unread_chat_count'] = ChatMessage.objects.filter(
            conversation__user=request.user, is_staff_reply=True, is_read=False,
        ).count()

    return context
