class UnicodeSlugConverter:
    """Same idea as Django's built-in 'slug' path converter, but accepting
    non-ASCII letters too.

    Post.slug (apps/blog/models.py) is generated via
    slugify(title, allow_unicode=True) so a Persian title keeps a Persian
    slug (e.g. "نوت-اول") instead of coming out empty. The built-in
    <slug:...> converter's regex is ASCII-only ([-a-zA-Z0-9_]+) and never
    matches that, which is exactly what broke reverse()/get_absolute_url()
    for any post with a non-ASCII slug. This regex mirrors Django's own
    validate_unicode_slug validator (used by SlugField(allow_unicode=True)
    itself) so anything the model considers a valid slug also matches here.
    """
    regex = r'[-\w]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
