"""
WSGI config for programminghunts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys
GEOIP_PATH =os.path.join('/var/www/programminghunts/geoip')
sys.path.append('/var/www/env/lib/python3.6/site-packages/')

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/programminghunts/')
# add the virtualenv site-packages path to the sys.path
# add the virtualenv site-packages path to the sys.path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programminghunts.settings')

application = get_wsgi_application()
