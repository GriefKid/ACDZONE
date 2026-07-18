"""
ASGI config for acdzone project.

Exposes the ASGI callable as a module-level variable named ``application``.
Used by async servers (uvicorn/daphne) if the project ever needs websockets
or async views.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acdzone.settings')

application = get_asgi_application()
