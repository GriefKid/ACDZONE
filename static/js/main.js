// ACD Zone front-end scripts.
// Bootstrap's own JS bundle (loaded in base.html) already handles the
// navbar toggler, dropdowns, and dismissible alerts. This file only adds
// small, dependency-free UI polish: active nav-link highlighting, a
// scroll-aware "glass" header state, and a scroll-reveal animation.

document.addEventListener('DOMContentLoaded', function () {
  // Re-run the server-side connection check after the visitor turns off VPN.
  var vpnRetryButton = document.getElementById('acdVpnRetry');
  if (vpnRetryButton) {
    vpnRetryButton.addEventListener('click', function () {
      vpnRetryButton.disabled = true;
      vpnRetryButton.classList.add('is-checking');
      vpnRetryButton.innerHTML =
        '<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>' +
        '<span>' + vpnRetryButton.dataset.rechecking + '</span>';
      window.location.reload();
    });
  }

  // Highlight the current page's nav link.
  var links = document.querySelectorAll('.navbar-nav .nav-link');
  links.forEach(function (link) {
    if (link.getAttribute('href') === window.location.pathname) {
      link.classList.add('active');
    }
  });

  // Glass header gains a stronger/more opaque background once the page has
  // scrolled a bit, so it reads clearly over any content behind it.
  var header = document.querySelector('.acd-header');
  if (header) {
    var applyScrollState = function () {
      if (window.scrollY > 24) {
        header.classList.add('is-scrolled');
      } else {
        header.classList.remove('is-scrolled');
      }
    };
    applyScrollState();
    window.addEventListener('scroll', applyScrollState, { passive: true });
  }

  // Scroll-reveal: any element with class="acd-reveal" fades/slides into
  // place the first time it enters the viewport. Falls back to instantly
  // visible if IntersectionObserver isn't available.
  var revealTargets = document.querySelectorAll('.acd-reveal');
  if (revealTargets.length) {
    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
      );
      revealTargets.forEach(function (el) { observer.observe(el); });
    } else {
      revealTargets.forEach(function (el) { el.classList.add('is-visible'); });
    }
  }

  // Auth-required modal (templates/partials/auth_required_modal.html):
  // signed-out visitors get this instead of an immediate redirect when they
  // click "خرید" on ACDPay/ACDBallons. The trigger button carries
  // data-login-url/data-signup-url — each already baked with ?next=<that
  // product's own buy URL> (see templates/shop/acdpay.html /
  // acdballoons.html) — so copy them onto the modal's two buttons right as
  // it opens. event.relatedTarget is the exact button that was clicked,
  // per the Bootstrap modal show.bs.modal event contract, so this works
  // correctly no matter which product card triggered it.
  var authModal = document.getElementById('authRequiredModal');
  if (authModal) {
    authModal.addEventListener('show.bs.modal', function (event) {
      var trigger = event.relatedTarget;
      if (!trigger) return;
      var loginBtn = document.getElementById('authRequiredModalLoginBtn');
      var signupBtn = document.getElementById('authRequiredModalSignupBtn');
      var loginUrl = trigger.getAttribute('data-login-url');
      var signupUrl = trigger.getAttribute('data-signup-url');
      if (loginBtn && loginUrl) loginBtn.setAttribute('href', loginUrl);
      if (signupBtn && signupUrl) signupBtn.setAttribute('href', signupUrl);
    });
  }

  // Welcome mascot (templates/partials/welcome_mascot.html): a permanent
  // fixture now, on every page, for every visitor (logged in or not) — no
  // "seen once" localStorage gate and no auto-hide timer. It just plays
  // its entrance + wave once per page load, then stays put. The close
  // button only hides it for this particular page view (it comes back on
  // the next page/reload), so there's still an escape route without
  // undermining "always there".
  var mascot = document.getElementById('acdMascotWidget');
  if (mascot) {
    // Small delay so it doesn't compete with the page's own entrance/
    // reveal animations for attention in the very first instant.
    window.setTimeout(function () {
      mascot.classList.add('is-visible');
    }, 900);

    var closeBtn = document.getElementById('acdMascotClose');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        mascot.classList.remove('is-visible');
      });
    }
  }

  // Country page travel-route calculator (templates/core/country_detail.html):
  // all of this country's active TravelRoute rows already sit in the DOM as
  // one JSON blob (data-routes), serialized server-side in
  // apps/core/views.py's country_detail() — no request needed here, this
  // just filters that array client-side by the two selects the visitor
  // picks and reveals whichever result div matches.
  var routeCalc = document.querySelector('.acd-route-calc');
  if (routeCalc) {
    var routes = [];
    try {
      routes = JSON.parse(routeCalc.getAttribute('data-routes') || '[]');
    } catch (e) {
      routes = [];
    }
    var originSelect = document.getElementById('acdRouteOrigin');
    var modeSelect = document.getElementById('acdRouteMode');
    var showBtn = document.getElementById('acdRouteShow');
    var resultBox = document.getElementById('acdRouteResult');
    var emptyBox = document.getElementById('acdRouteEmpty');

    if (showBtn && originSelect && modeSelect && resultBox && emptyBox) {
      showBtn.addEventListener('click', function () {
        var originId = originSelect.value;
        var mode = modeSelect.value;

        resultBox.classList.add('d-none');
        emptyBox.classList.add('d-none');

        if (!originId || !mode) {
          emptyBox.classList.remove('d-none');
          return;
        }

        var match = routes.find(function (route) {
          return String(route.origin_id) === String(originId) && route.mode === mode;
        });

        if (!match) {
          emptyBox.classList.remove('d-none');
          return;
        }

        var distanceLabel = match.distance_km
          ? Number(match.distance_km).toLocaleString() + ' km'
          : '';
        var pieces = [];
        if (distanceLabel) {
          pieces.push(
            '<div class="acd-route-result-distance">' + distanceLabel +
            (match.is_estimate ? ' <span class="acd-route-estimate-badge">~</span>' : '') +
            '</div>'
          );
        }
        // duration_text for computed (is_estimate) entries already includes
        // "(تخمینی)"/"(estimated)" wording itself (see apps/core/geo.py),
        // so no extra i18n lookup is needed here.
        if (match.duration_text) pieces.push('<div class="acd-route-result-duration">' + match.duration_text + '</div>');
        if (match.notes) pieces.push('<div class="acd-route-result-notes">' + match.notes + '</div>');

        resultBox.innerHTML =
          '<span class="acd-route-result-icon"><i class="bi bi-' + (match.icon || 'signpost-2') + '"></i></span>' +
          '<div>' + pieces.join('') + '</div>';
        resultBox.classList.remove('d-none');
      });
    }
  }
});
