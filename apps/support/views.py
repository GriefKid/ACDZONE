from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timesince import timesince
from django.views.decorators.http import require_GET, require_POST

from apps.core.translations import translate

from .forms import TicketCreateForm
from .models import ChatMessage, Conversation, Ticket, TicketMessage


@login_required
def ticket_list(request):
    tickets = request.user.tickets.all()
    return render(request, 'support/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(user=request.user, subject=form.cleaned_data['subject'])
            # First message on a new ticket — Ticket.save() itself never
            # sends any notification; TicketMessage.save() covers "new
            # ticket" as a special case of "first non-staff message" (see
            # apps/support/models.py). is_staff_reply=False explicitly:
            # this form is only ever the customer's own, even if the
            # logged-in account happens to also have is_staff=True.
            TicketMessage.objects.create(
                ticket=ticket, sender=request.user, body=form.cleaned_data['body'], is_staff_reply=False,
            )
            messages.success(request, translate('تیکت شما ثبت شد؛ پشتیبانی به‌زودی پاسخ می‌دهد.'))
            return redirect(ticket.get_absolute_url())
    else:
        form = TicketCreateForm()
    return render(request, 'support/ticket_form.html', {'form': form})


@login_required
def ticket_detail(request, pk):
    # Read-only on purpose: a ticket is submitted once, and from here on
    # only staff can add to it (from /admin/ — see apps/support/admin.py's
    # TicketMessageInline). The customer just watches the thread and gets
    # a bell notification (apps/support/models.py TicketMessage.save())
    # the moment support replies. No reply form, no POST handling here.
    #
    # Scoped to request.user so nobody can view another user's ticket by
    # guessing a pk in the URL.
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'ticket_messages': ticket.messages.select_related('sender'),
    })


# --- Floating chat widget (AJAX) --------------------------------------
#
# Three small JSON endpoints power templates/partials/chat_widget.html:
#   - chat_unread_count: polled quietly in the background on every page,
#     just to keep the little badge on the closed bubble accurate. Never
#     marks anything as read — a passive poll must not consume a
#     notification the person hasn't actually looked at yet.
#   - chat_messages: called when the widget is actually opened (and then
#     re-polled while it stays open). Returns the full thread AND marks
#     any unread staff replies as read, since opening the panel IS
#     looking at them.
#   - chat_send: posts a new customer message. Always is_staff_reply=False
#     — the customer is the only one who ever posts here. Staff replies
#     exclusively through /admin/ (see ConversationAdmin.save_formset in
#     apps/support/admin.py), same division as the ticket system.
#
# Conversation is looked up via request.user.chat_conversation, the
# reverse OneToOneField accessor. When it doesn't exist yet (a user who
# has never opened the widget), Django raises Conversation.DoesNotExist
# — NOT a plain AttributeError — so this is a real try/except, not a
# getattr(..., None) shortcut.

@login_required
@require_GET
def chat_unread_count(request):
    count = ChatMessage.objects.filter(
        conversation__user=request.user, is_staff_reply=True, is_read=False,
    ).count()
    return JsonResponse({'count': count})


@login_required
@require_GET
def chat_messages(request):
    try:
        conversation = request.user.chat_conversation
    except Conversation.DoesNotExist:
        return JsonResponse({'messages': []})

    conversation.messages.filter(is_staff_reply=True, is_read=False).update(is_read=True)

    payload = [
        {
            'id': msg.pk,
            'body': msg.body,
            'is_staff_reply': msg.is_staff_reply,
            'sender_label': translate('پشتیبانی') if msg.is_staff_reply else translate('شما'),
            'time_label': f'{timesince(msg.created_at)} {translate("پیش")}',
        }
        for msg in conversation.messages.all()
    ]
    return JsonResponse({'messages': payload})


@login_required
@require_POST
def chat_send(request):
    body = request.POST.get('body', '').strip()
    if not body:
        return JsonResponse({'error': translate('متن پیام نمی‌تواند خالی باشد.')}, status=400)

    conversation, _created = Conversation.objects.get_or_create(user=request.user)
    ChatMessage.objects.create(
        conversation=conversation, sender=request.user, body=body, is_staff_reply=False,
    )
    return JsonResponse({'ok': True})
