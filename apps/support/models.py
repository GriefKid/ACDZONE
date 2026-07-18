from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.core.models import Notification
from apps.core.translations import translate_lazy as _

STATUS_OPEN = 'open'
STATUS_ANSWERED = 'answered'
STATUS_CLOSED = 'closed'
STATUS_CHOICES = [
    (STATUS_OPEN, 'باز'),
    (STATUS_ANSWERED, 'پاسخ داده شده'),
    (STATUS_CLOSED, 'بسته شده'),
]


class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tickets', verbose_name=_('کاربر'),
    )
    subject = models.CharField(_('موضوع'), max_length=200)
    status = models.CharField(_('وضعیت'), max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(_('تاریخ ثبت'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین بروزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت‌ها')
        ordering = ['-updated_at']

    def __str__(self):
        return f'#{self.pk} · {self.subject}'

    def get_absolute_url(self):
        return reverse('support:ticket_detail', args=[self.pk])


class TicketMessage(models.Model):
    """
    One line of the conversation. `is_staff_reply` decides everything in
    save() below (who gets notified, which way the ticket's status flips)
    — and it's set EXPLICITLY by whichever code path creates the message
    (apps/support/views.ticket_create always passes False; apps/support/
    admin.py's save_formset always passes True for a new inline row), not
    inferred from sender.is_staff.

    That distinction matters: this project's own staff/superuser accounts
    are also perfectly normal site users (nothing stops the site owner
    from testing the customer-facing ticket form with their own admin
    login) — inferring "is this a staff reply?" from sender.is_staff would
    have meant a staff member's own opening question, submitted through
    the ordinary front-end form, got misread as if support had already
    answered it. Explicit beats inferred here.
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name=_('تیکت'))
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='ticket_messages', verbose_name=_('فرستنده'),
    )
    body = models.TextField(_('متن پیام'))
    is_staff_reply = models.BooleanField(_('پاسخ پشتیبانی'), default=False)
    created_at = models.DateTimeField(_('تاریخ ارسال'), auto_now_add=True)

    class Meta:
        verbose_name = _('پیام تیکت')
        verbose_name_plural = _('پیام‌های تیکت')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} · {self.body[:40]}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new:
            return

        # First message on a brand-new ticket goes through here too — a
        # "new ticket" IS just "first (non-staff-reply) message", so
        # there's no separate Ticket-level notification path needed.
        if self.is_staff_reply:
            self.ticket.status = STATUS_ANSWERED
            self.ticket.save(update_fields=['status', 'updated_at'])
            Notification.objects.create(
                user=self.ticket.user,
                message=f'پشتیبانی به تیکت «{self.ticket.subject}» پاسخ داد.',
                link=self.ticket.get_absolute_url(),
            )
        else:
            # Reopens an answered/closed ticket the same way a fresh reply
            # from the customer naturally would; no-op if it was already open.
            self.ticket.status = STATUS_OPEN
            self.ticket.save(update_fields=['status', 'updated_at'])
            User = get_user_model()
            Notification.objects.bulk_create([
                Notification(
                    user=staff,
                    message=f'پیام جدید در تیکت «{self.ticket.subject}» از {self.sender}.',
                    link=self.ticket.get_absolute_url(),
                )
                for staff in User.objects.filter(is_staff=True, is_active=True)
            ])


class Conversation(models.Model):
    """
    One shared live-chat thread per customer with "admin" — defined, per
    the user's own words, as anyone who can log into the Django admin
    (is_staff=True). Not per-staff-member: any staff member can read and
    reply from the admin panel, exactly mirroring Ticket/TicketMessage's
    one-thread-many-staff model above.

    Created lazily (get_or_create) the first time a user sends a message
    from the floating widget, so users who never open the chat never get
    a row here.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chat_conversation', verbose_name=_('کاربر'),
    )
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین پیام'), auto_now=True)

    class Meta:
        verbose_name = _('گفتگو')
        verbose_name_plural = _('گفتگوها')
        ordering = ['-updated_at']

    def __str__(self):
        return f'گفتگو با {self.user}'


class ChatMessage(models.Model):
    """
    One line inside a Conversation. Same explicit-field lesson as
    TicketMessage.is_staff_reply above, learned the hard way on this
    project: is_staff_reply is set by whichever code path CREATES the
    message — apps/support/views.chat_send always passes False,
    apps/support/admin.py's ConversationAdmin save_formset always passes
    True for a new inline row — and is never inferred from
    sender.is_staff. There is no admin-facing chat widget, so those are
    the only two creation sites, same as the Ticket precedent.

    is_read tracks whether the addressee has actually opened the widget
    to see a given message (used for the small unread badge on the
    floating bubble itself, customer side) — or, for a customer's own
    message, whether staff have opened that conversation in the admin
    (used for the "پیام‌های بی‌پاسخ" count there — see
    apps/support/admin.py ConversationAdmin).

    No sitewide Notification (bell) is fired here on purpose — chat
    already has its own dedicated, live counters on both sides (the
    widget's own badge for the customer, the admin's list column +
    sidebar badge for staff), so a bell entry on top would just be a
    redundant second notice — and for staff specifically, not even a
    reliable one, since the bell only lives in the PUBLIC site's header,
    not inside /admin/ at all.
    """
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE,
        related_name='messages', verbose_name=_('گفتگو'),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chat_messages', verbose_name=_('فرستنده'),
    )
    body = models.TextField(_('متن پیام'))
    is_staff_reply = models.BooleanField(_('پاسخ پشتیبانی'), default=False)
    is_read = models.BooleanField(_('خوانده‌شده'), default=False)
    telegram_message_id = models.BigIntegerField(
        _('شناسه پیام تلگرام'), null=True, blank=True,
        help_text='برای همگام‌سازی داخلی با گروه پشتیبانی تلگرام — دستی پر نکنید.',
    )
    created_at = models.DateTimeField(_('تاریخ ارسال'), auto_now_add=True)

    class Meta:
        verbose_name = _('پیام گفتگو')
        verbose_name_plural = _('پیام‌های گفتگو')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} · {self.body[:40]}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new:
            return

        # auto_now on Conversation.updated_at only fires from Conversation's
        # own .save() — creating a ChatMessage doesn't touch its parent row
        # by itself, so bump it explicitly. Keeps the admin's Conversation
        # changelist (ordered -updated_at) sorted by "most recently active"
        # instead of "most recently created", which matters once a
        # conversation gets replies.
        #
        # Deliberately nothing else here — see the class docstring above
        # for why this doesn't also fire a Notification like
        # TicketMessage.save() does.
        Conversation.objects.filter(pk=self.conversation_id).update(updated_at=timezone.now())

        # Telegram bridge, customer -> Telegram half only (see
        # apps/support/telegram_bot.py and the poll_telegram management
        # command for the other half — staff replying IN Telegram). Only
        # customer messages get pushed out; pushing staff replies too
        # would just echo back into the same group whatever a staff
        # member had just typed there. send_message() is a safe no-op
        # (returns None) if Telegram hasn't been configured in .env yet —
        # the on-site widget must keep working with zero Telegram setup.
        if not self.is_staff_reply:
            from apps.support.telegram_bot import send_message
            text = f'پیام جدید از {self.sender} (گفتگو #{self.conversation_id}):\n\n{self.body}'
            telegram_message_id = send_message(text)
            if telegram_message_id:
                ChatMessage.objects.filter(pk=self.pk).update(telegram_message_id=telegram_message_id)


class TelegramBotState(models.Model):
    """
    Single-row table (always pk=1 — see .load() below) holding just the
    Telegram getUpdates cursor. The poll_telegram management command (run
    every minute or so via cron, see README) needs to remember, between
    completely separate process runs, which updates it has already
    applied — a plain Python variable wouldn't survive past one run, and
    Django's cache framework isn't guaranteed to persist across a server
    restart either. The database is the one thing already guaranteed to
    be there and durable, so a tiny dedicated model beats a stray file on
    disk (which would also complicate deployment: one more path to get
    right, one more thing that could have wrong permissions).
    """
    last_update_id = models.BigIntegerField(_('آخرین شناسه پردازش‌شده'), default=0)

    class Meta:
        verbose_name = _('وضعیت بات تلگرام')
        verbose_name_plural = _('وضعیت بات تلگرام')

    def __str__(self):
        return f'Telegram bot state (last_update_id={self.last_update_id})'

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj
