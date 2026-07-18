// ACD Zone — live notification bell (header, every page for logged-in
// users). Same reasoning and shape as static/js/chat-widget.js: polling
// only, no websockets. One real behavioral difference from the chat
// widget on purpose — merely OPENING this dropdown does NOT mark
// anything read (unlike opening the chat panel). The bell's individual
// items are only marked read by actually clicking one (still a plain
// navigation to notification_open, unchanged) or by the explicit
// "mark all as read" button — so simply glancing at what's new here
// never silently consumes the badge count.

document.addEventListener('DOMContentLoaded', function () {
  var menuEl = document.getElementById('acd-notif-menu');
  var toggleBtn = document.getElementById('acd-notif-toggle');
  if (!menuEl || !toggleBtn) {
    // Not rendered for anonymous visitors (see templates/partials/header.html).
    return;
  }

  var badgeEl = document.getElementById('acd-notif-badge');
  var emptyItem = document.getElementById('acd-notif-empty-item');
  var dividerItem = document.getElementById('acd-notif-divider');
  var markAllItem = document.getElementById('acd-notif-mark-all-item');
  var markAllBtn = document.getElementById('acd-notif-mark-all');

  var unreadUrl = menuEl.dataset.unreadUrl;
  var listUrl = menuEl.dataset.listUrl;
  var markAllUrl = menuEl.dataset.markAllUrl;

  var CLOSED_POLL_MS = 20000;
  var OPEN_POLL_MS = 8000;
  var pollTimer = null;

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  // Same Django-documented CSRF-cookie-reading snippet as
  // chat-widget.js. Kept as its own copy rather than a shared helper —
  // it's small, unlikely to change, and duplicating it here means this
  // file has zero risk of disturbing the already-reviewed chat widget.
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
        // Silent — background poll hiccup, retried next tick.
      });
  }

  function buildNotificationNode(note) {
    var li = document.createElement('li');
    li.className = 'acd-notif-li';

    var a = document.createElement('a');
    a.className = 'dropdown-item acd-notif-item' + (note.is_read ? '' : ' acd-notif-unread');
    a.href = note.open_url;

    var message = document.createElement('span');
    message.className = 'acd-notif-message';
    message.textContent = note.message;

    var time = document.createElement('span');
    time.className = 'acd-notif-time';
    time.textContent = note.time_label;

    a.appendChild(message);
    a.appendChild(time);
    li.appendChild(a);
    return li;
  }

  function renderNotifications(list) {
    // Only the dynamic items carry this class — the empty/divider/mark-
    // all <li>s are fixed elements this function just shows or hides,
    // never removes, so it can't accidentally drop them.
    var existing = menuEl.querySelectorAll('.acd-notif-li');
    existing.forEach(function (li) { li.remove(); });

    var hasItems = !!(list && list.length);

    if (emptyItem) {
      if (hasItems) { emptyItem.classList.add('d-none'); } else { emptyItem.classList.remove('d-none'); }
    }
    if (dividerItem) {
      if (hasItems) { dividerItem.classList.remove('d-none'); } else { dividerItem.classList.add('d-none'); }
    }
    if (markAllItem) {
      if (hasItems) { markAllItem.classList.remove('d-none'); } else { markAllItem.classList.add('d-none'); }
    }

    if (hasItems && dividerItem) {
      list.forEach(function (note) {
        dividerItem.parentNode.insertBefore(buildNotificationNode(note), dividerItem);
      });
    }
  }

  function loadNotifications() {
    fetch(listUrl, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        renderNotifications(data.notifications || []);
        // Piggybacked on the same response (apps/core/views.py
        // notifications_list) — merely opening the dropdown must NOT
        // change the count itself, but a genuinely new notification
        // that arrived since the last full page load should still show
        // up in the badge once we've fetched this far anyway.
        updateBadge(data.unread_count || 0);
      })
      .catch(function () {
        // Silent — dropdown just keeps showing whatever it already had.
      });
  }

  toggleBtn.addEventListener('shown.bs.dropdown', function () {
    stopPolling();
    loadNotifications();
    pollTimer = setInterval(loadNotifications, OPEN_POLL_MS);
  });

  toggleBtn.addEventListener('hidden.bs.dropdown', function () {
    stopPolling();
    pollUnreadCount();
    pollTimer = setInterval(pollUnreadCount, CLOSED_POLL_MS);
  });

  if (markAllBtn) {
    markAllBtn.addEventListener('click', function () {
      markAllBtn.disabled = true;
      fetch(markAllUrl, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      })
        .then(function (r) {
          if (!r.ok) {
            throw new Error('mark-all-read failed');
          }
          return r.json();
        })
        .then(function () {
          updateBadge(0);
          var unread = menuEl.querySelectorAll('.acd-notif-item.acd-notif-unread');
          unread.forEach(function (item) { item.classList.remove('acd-notif-unread'); });
        })
        .catch(function () {
          // Silent — worst case nothing changed locally; the next poll
          // or the next time the dropdown opens reconciles with the
          // server anyway, and the person can just click it again.
        })
        .finally(function () {
          markAllBtn.disabled = false;
        });
    });
  }

  // Baseline: cheap badge check now, then settle into the closed-panel
  // polling cadence (mirrors chat-widget.js's own startup sequence).
  pollUnreadCount();
  pollTimer = setInterval(pollUnreadCount, CLOSED_POLL_MS);
});
