import os

from django.core.asgi import get_asgi_application
from daphne import server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django_application = get_asgi_application()



