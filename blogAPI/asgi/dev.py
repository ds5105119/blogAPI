from .base import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogAPI.settings.dev')

application = get_asgi_application()
