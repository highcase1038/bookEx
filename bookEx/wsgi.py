"""
WSGI config for bookEx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookEx.settings')

application = get_wsgi_application()
"""

import sys
import os

path = '/home/Jcode/bookEx'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookEx.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
