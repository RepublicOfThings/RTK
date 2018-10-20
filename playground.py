'''
"""
WSGI config for RTKWebApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# sys.path.append('/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects')
sys.path.append('/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects/haltoncouncil/')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects/haltoncouncil/egg_cache")

os.environ["DJANGO_SETTINGS_MODULE"] = "HaltoncouncilWebApp.settings"

application = get_wsgi_application()

'''