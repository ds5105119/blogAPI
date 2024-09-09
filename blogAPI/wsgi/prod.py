from .base import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogAPI.settings.prod')

application = get_wsgi_application()
