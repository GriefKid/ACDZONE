"""
WSGI config for acdzone project.

Exposes the WSGI callable as a module-level variable named ``application``.
Used by traditional (non-async) production servers such as gunicorn/waitress.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acdzone.settings')

application = get_wsgi_application()
