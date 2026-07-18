from django.shortcuts import get_object_or_404, render

from .models import CATEGORY_CHOICES, CATEGORY_ICONS, CHANNEL_NEWS, CHANNEL_NOTES, Post


def _active_posts(channel):
    return Post.objects.filter(is_active=True, channel=channel)


def acdnews(request):
    active_category = request.GET.get('category', '')
    # Separate query param, not a 5th CATEGORY_CHOICES value — is_urgent is a
    # flag orthogonal to category (a sports story can also be urgent), so it
    # filters instead of replacing the category system.
    show_urgent_only = request.GET.get('urgent') == '1'

    posts = _active_posts(CHANNEL_NEWS)
    if show_urgent_only:
        posts = posts.filter(is_urgent=True)
    elif active_category:
        posts = posts.filter(category=active_category)
    # Urgent posts always float to the top regardless of published_at, in
    # every view (all / a single category / urgent-only itself).
    posts = posts.order_by('-is_urgent', '-published_at')

    context = {
        'posts': posts,
        'active_category': active_category,
        'show_urgent_only': show_urgent_only,
        # Pre-zipped with icons here so the template doesn't need a custom
        # dict-lookup filter — see apps/blog/models.py for the source lists.
        'category_pills': [
            {'key': key, 'label': label, 'icon': CATEGORY_ICONS.get(key, 'tag')}
            for key, label in CATEGORY_CHOICES
        ],
    }
    return render(request, 'blog/acdnews.html', context)


def news_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, channel=CHANNEL_NEWS, is_active=True)
    return render(request, 'blog/news_detail.html', {'post': post})


def acdnotes(request):
    posts = _active_posts(CHANNEL_NOTES).order_by('-is_urgent', '-published_at')
    return render(request, 'blog/acdnotes.html', {'posts': posts})


def notes_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, channel=CHANNEL_NOTES, is_active=True)
    return render(request, 'blog/notes_detail.html', {'post': post})
