"""
WSGI config for beenquickServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beenquickServer.settings")
application = get_wsgi_application()
