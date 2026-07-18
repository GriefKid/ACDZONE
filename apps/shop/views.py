import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.translations import translate

from .forms import OrderRequestForm
from .models import ACDPAY_STAGE_FLOW, Order, PAGE_ACDBALLOONS, PAGE_ACDPAY, Product, STAGE_LABELS

# Same idea as apps/core/views.py's home() intro video: drop the file here
# under this exact name (and the optional Persian subtitle track next to
# it) and the page starts playing it automatically — no code change needed.
ACDPAY_VIDEO_REL_PATH = 'video/acdpay-intro.mp4'
ACDPAY_SUBTITLE_REL_PATH = 'video/acdpay-intro-fa.vtt'
ACDBALLOONS_VIDEO_REL_PATH = 'video/acdballoons-intro.mp4'
ACDBALLOONS_SUBTITLE_REL_PATH = 'video/acdballoons-intro-fa.vtt'


def _media_exists(rel_path):
    return os.path.exists(os.path.join(settings.BASE_DIR, 'static', rel_path))


def _active_products(page):
    return (
        Product.objects.filter(is_active=True, category__page=page, category__is_active=True)
        .select_related('category')
    )


def acdpay(request):
    products = list(_active_products(PAGE_ACDPAY))
    context = {
        'products': products,
        # Per-product full-length copy, shown as an accordion further down
        # the page. Falls back to a generic paragraph when nothing has
        # long_description filled in yet.
        'products_with_info': [p for p in products if p.long_description],
        'intro_video_exists': _media_exists(ACDPAY_VIDEO_REL_PATH),
        'intro_subtitle_exists': _media_exists(ACDPAY_SUBTITLE_REL_PATH),
    }
    return render(request, 'shop/acdpay.html', context)


def acdballoons(request):
    context = {
        'products': _active_products(PAGE_ACDBALLOONS),
        'intro_video_exists': _media_exists(ACDBALLOONS_VIDEO_REL_PATH),
        'intro_subtitle_exists': _media_exists(ACDBALLOONS_SUBTITLE_REL_PATH),
    }
    return render(request, 'shop/acdballoons.html', context)


@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            messages.success(
                request,
                translate('درخواست خرید شما ثبت شد؛ همکاران ما به‌زودی پیگیری می‌کنند.'),
            )
            return redirect('shop:order_detail', pk=order.pk)
    else:
        form = OrderRequestForm(initial={
            'full_name': request.user.get_full_name() or request.user.get_username(),
            'contact_number': getattr(request.user, 'phone_number', ''),
            'email': request.user.email,
        })

    return render(request, 'shop/buy.html', {'form': form, 'product': product})


@login_required
def my_products(request):
    orders = (
        Order.objects.filter(user=request.user, is_hidden=False)
        .select_related('product', 'product__category')
    )
    context = {
        'orders': orders,
        # Only used by the empty-state preview, to show a first-time buyer
        # what to expect after purchasing an ACDPay card.
        'acdpay_stage_preview': [STAGE_LABELS[key] for key in ACDPAY_STAGE_FLOW],
    }
    return render(request, 'shop/my_products.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related('product', 'product__category'),
        pk=pk, user=request.user,
    )
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        order.is_hidden = True
        order.save(update_fields=['is_hidden'])
        messages.success(request, translate('محصول از لیست حذف شد.'))
    return redirect('shop:my_products')
