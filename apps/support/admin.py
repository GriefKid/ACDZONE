from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from apps.core.translations import translate_lazy as _

from .models import ChatMessage, Conversation, Ticket, TicketMessage


class TicketMessageInline(TabularInline):
    """
    Existing messages plus one empty row for the staff member's reply.

    `sender` is deliberately NOT in `fields` — it's auto-assigned to the
    logged-in staff user in TicketAdmin.save_formset() below (which also
    sets is_staff_reply=True there — anything created through this inline
    is, by definition, a staff reply, regardless of whether the logged-in
    admin account happens to also be the ticket's own customer). The
    read-only `sender_label` column shows who actually sent each existing
    line instead.

    Trade-off accepted on purpose: `body` stays editable on existing rows
    too (Django admin inlines don't cleanly support "old rows read-only,
    only the new row editable" without real formset surgery). This is an
    internal tool for the site's own trusted staff, not a public-facing
    edit history, so that's fine — same trust model as Order.stage being
    directly list_editable elsewhere in this project.
    """
    model = TicketMessage
    extra = 1
    can_delete = False
    fields = ('sender_label', 'body', 'created_at')
    readonly_fields = ('sender_label', 'created_at')

    def sender_label(self, obj):
        if obj and obj.pk:
            return str(obj.sender)
        return '—'
    sender_label.short_description = _('فرستنده')


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ('subject', 'user', 'status', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status',)
    search_fields = ('subject', 'user__username')
    readonly_fields = ('user', 'created_at')
    inlines = [TicketMessageInline]
    fieldsets = (
        (None, {'fields': (('user', 'status'), 'subject', 'created_at')}),
    )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TicketMessage) and not instance.pk:
                instance.sender = request.user
                instance.is_staff_reply = True
            instance.save()
        formset.save_m2m()


class ChatMessageInline(TabularInline):
    """
    Same shape and same reasoning as TicketMessageInline above: `sender`
    is deliberately absent from `fields` (auto-assigned to the logged-in
    staff user in ConversationAdmin.save_formset() below, which also sets
    is_staff_reply=True there unconditionally — anything created through
    this inline is by definition a staff reply). `sender_label` shows who
    actually sent each existing line.
    """
    model = ChatMessage
    extra = 1
    can_delete = False
    fields = ('sender_label', 'body', 'created_at')
    readonly_fields = ('sender_label', 'created_at')

    def sender_label(self, obj):
        if obj and obj.pk:
            return str(obj.sender)
        return '—'
    sender_label.short_description = _('فرستنده')


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ('user', 'unanswered_count', 'updated_at', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'created_at')
    inlines = [ChatMessageInline]
    fieldsets = (
        (None, {'fields': ('user', 'created_at')}),
    )

    @admin.display(description=_('پیام‌های بی‌پاسخ'))
    def unanswered_count(self, obj):
        # Plain inline styles rather than Tailwind utility classes on
        # purpose — Unfold's compiled CSS only ships the utility classes
        # IT actually uses internally, not the full Tailwind set (this is
        # exactly what made admin-custom.css necessary earlier for RTL
        # fixes), so a class typed here might silently not exist at all.
        # Inline styles always render regardless of what got compiled.
        count = obj.messages.filter(is_staff_reply=False, is_read=False).count()
        if count:
            return format_html(
                '<span style="display:inline-flex;align-items:center;justify-content:center;'
                'min-width:1.6rem;height:1.6rem;padding:0 0.45rem;border-radius:999px;'
                'background:#dc2626;color:#fff;font-weight:700;font-size:0.8rem;">{}</span>',
                count,
            )
        return format_html('<span style="opacity:0.45;">0</span>')

    def has_add_permission(self, request):
        # A Conversation is only ever created lazily by a customer's own
        # first widget message (apps/support/views.chat_send) — staff
        # creating one out of thin air here would leave it with no
        # customer message and nothing sensible to reply to.
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Opening a conversation IS "staff has seen these" — mark every
        # unread customer message read right away, mirroring exactly how
        # apps/support/views.chat_messages marks staff replies read the
        # moment the customer opens their widget. Runs before super() so
        # it's in effect whether this request ends up being a plain GET
        # (viewing) or a POST (saving a reply) — either way, staff has by
        # now definitely seen what was here.
        ChatMessage.objects.filter(
            conversation_id=object_id, is_staff_reply=False, is_read=False,
        ).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ChatMessage) and not instance.pk:
                instance.sender = request.user
                instance.is_staff_reply = True
            instance.save()
        formset.save_m2m()
