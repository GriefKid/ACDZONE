from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, SignUpForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = 'core:home'


def signup(request):
    # Mirrors LoginView's own ?next= handling (see the auth-required modal,
    # templates/partials/auth_required_modal.html: its "عضو شوید" link
    # points here with ?next=<the buy page the visitor was trying to
    # reach>) so signing up sends a new member straight back to checkout
    # instead of dropping them on the homepage. The hidden field in
    # signup.html carries it through the POST too, since a query string on
    # the page's own URL doesn't survive a form submit on its own.
    next_url = request.POST.get('next') or request.GET.get('next') or 'core:home'
    # Same open-redirect guard Django's own LoginView applies to its ?next=
    # (django.contrib.auth.views.LoginView.get_success_url) — without it,
    # someone could hand a victim a signup link with next=https://evil.com
    # and get them redirected off-site right after they log in.
    if next_url != 'core:home' and not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure(),
    ):
        next_url = 'core:home'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'next': next_url})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
