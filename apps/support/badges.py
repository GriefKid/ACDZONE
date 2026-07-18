"""
Sidebar badge callbacks (acdzone/settings.py UNFOLD['SIDEBAR']).

Unfold resolves a navigation item's 'badge' key by import_string-ing it
and calling callback(request) — see venv's unfold/sites.py
_get_navigation_items(). That's the only shape it accepts (a dotted
import path to a callable), so this lives in its own tiny module rather
than as a method somewhere, and takes `request` even though the count
below doesn't need it — any staff member can answer any conversation
(shared inbox, not per-agent assignment, exactly like ACDSupport
tickets), so the count is global, not scoped to request.user.
"""
from .models import ChatMessage


def unanswered_chat_count(request):
    return ChatMessage.objects.filter(is_staff_reply=False, is_read=False).count()
