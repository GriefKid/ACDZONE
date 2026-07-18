// ACD Zone — floating "chat with admin" widget.
//
// AJAX polling only (no websockets/channels): a lightweight unread-count
// check while the panel is closed, switching to fetching the full thread
// (which also marks staff replies as read server-side) while it's open.
// Bootstrap's own dropdown/dropup component drives the open/close
// mechanics — this file only fetches data and renders it; it never
// manages the panel's show/hide state itself, and never touches
// innerHTML with anything that came from a message body (textContent
// only, to keep user-supplied text inert no matter what it contains).

document.addEventListener('DOMContentLoaded', function () {
  var widget = document.getElementById('acd-chat-widget');
  if (!widget) {
    // Not rendered at all for anonymous visitors (see chat_widget.html) —
    // this guard is just cheap extra safety against future changes.
    return;
  }

  var toggleBtn = document.getElementById('acd-chat-toggle');
  var badgeEl = document.getElementById('acd-chat-badge');
  var threadEl = document.getElementById('acd-chat-thread');
  var emptyEl = document.getElementById('acd-chat-empty');
  var listEl = document.getElementById('acd-chat-messages-list');
  var formEl = document.getElementById('acd-chat-form');
  var inputEl = document.getElementById('acd-chat-input');
  var sendBtn = document.getElementById('acd-chat-send');
  var errorEl = document.getElementById('acd-chat-error');

  var messagesUrl = widget.dataset.messagesUrl;
  var sendUrl = widget.dataset.sendUrl;
  var unreadUrl = widget.dataset.unreadUrl;
  var errorText = widget.dataset.errorText;

  var UNREAD_POLL_MS = 20000;
  var MESSAGES_POLL_MS = 5000;
  var pollTimer = null;

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  // Django's own documented pattern for reading the CSRF cookie for a
  // hand-rolled AJAX request (docs: "Using CSRF protection with AJAX").
  // The cookie itself is guaranteed to exist on every page thanks to
  // apps/core/context_processors.py calling get_token(request).
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function showError(message) {
    if (!errorEl) {
      return;
    }
    errorEl.textContent = message;
    errorEl.classList.remove('d-none');
  }

  function hideError() {
    if (!errorEl) {
      return;
    }
    errorEl.classList.add('d-none');
  }

  function updateBadge(count) {
    if (!badgeEl) {
      return;
    }
    if (count > 0) {
      badgeEl.textContent = count > 99 ? '99+' : String(count);
      badgeEl.classList.remove('d-none');
    } else {
      badgeEl.classList.add('d-none');
    }
  }

  function pollUnreadCount() {
    fetch(unreadUrl, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) { updateBadge(data.count || 0); })
      .catch(function () {
        // Silent on purpose — a background poll hiccup isn't something
        // the person is actively waiting on; it just retries next tick.
      });
  }

  function buildMessageNode(msg) {
    var row = document.createElement('div');
    row.className = 'acd-chat-row ' + (msg.is_staff_reply ? 'acd-chat-row-start' : 'acd-chat-row-end');

    var bubble = document.createElement('div');
    bubble.className = 'acd-chat-bubble ' + (msg.is_staff_reply ? 'acd-chat-bubble-staff' : 'acd-chat-bubble-user');

    var sender = document.createElement('span');
    sender.className = 'acd-chat-bubble-sender';
    sender.textContent = msg.sender_label;

    var body = document.createElement('div');
    body.className = 'acd-chat-bubble-body';
    body.textContent = msg.body;

    var meta = document.createElement('span');
    meta.className = 'acd-chat-bubble-meta';
    meta.textContent = msg.time_label;

    bubble.appendChild(sender);
    bubble.appendChild(body);
    bubble.appendChild(meta);
    row.appendChild(bubble);
    return row;
  }

  function renderMessages(list) {
    if (!listEl) {
      return;
    }
    // Clearing existing children this way is safe — the XSS risk is
    // specifically about injecting untrusted strings as markup, not
    // about removing nodes that are already there.
    listEl.innerHTML = '';

    if (!list || list.length === 0) {
      if (emptyEl) {
        emptyEl.classList.remove('d-none');
      }
    } else {
      if (emptyEl) {
        emptyEl.classList.add('d-none');
      }
      list.forEach(function (msg) {
        listEl.appendChild(buildMessageNode(msg));
      });
    }

    if (threadEl) {
      threadEl.scrollTop = threadEl.scrollHeight;
    }
  }

  function loadMessages() {
    fetch(messagesUrl, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        renderMessages(data.messages || []);
        // The GET to /chat/messages/ is exactly what marks staff replies
        // as read server-side (apps/support/views.chat_messages) —
        // reflect that in the badge right away instead of waiting for
        // the next background unread-count poll.
        updateBadge(0);
      })
      .catch(function () {
        // Silent here too — the panel just stays on whatever it last
        // rendered and tries again on the next open/poll tick.
      });
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('shown.bs.dropdown', function () {
      stopPolling();
      loadMessages();
      pollTimer = setInterval(loadMessages, MESSAGES_POLL_MS);
    });

    toggleBtn.addEventListener('hidden.bs.dropdown', function () {
      stopPolling();
      pollUnreadCount();
      pollTimer = setInterval(pollUnreadCount, UNREAD_POLL_MS);
    });
  }

  if (formEl) {
    formEl.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = inputEl ? inputEl.value.trim() : '';
      if (!text) {
        return;
      }

      hideError();
      if (inputEl) { inputEl.disabled = true; }
      if (sendBtn) { sendBtn.disabled = true; }

      var body = new FormData();
      body.append('body', text);

      fetch(sendUrl, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: body,
      })
        .then(function (r) {
          if (!r.ok) {
            throw new Error('chat send failed');
          }
          return r.json();
        })
        .then(function () {
          if (inputEl) { inputEl.value = ''; }
          loadMessages();
        })
        .catch(function () {
          showError(errorText);
        })
        .finally(function () {
          if (inputEl) { inputEl.disabled = false; }
          if (sendBtn) { sendBtn.disabled = false; }
          if (inputEl) { inputEl.focus(); }
        });
    });
  }

  // Baseline state on every page load: just the cheap badge check, then
  // settle into the closed-panel polling cadence.
  pollUnreadCount();
  pollTimer = setInterval(pollUnreadCount, UNREAD_POLL_MS);
});
