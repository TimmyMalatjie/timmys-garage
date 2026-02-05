"""
Vercel WSGI handler for Django
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timmys_garage.settings')

# Generate favicon before first request
try:
    from generate_favicon import create_favicon_ico
    create_favicon_ico()
except Exception:
    pass

# Collect static files
import subprocess
try:
    subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=False)
except Exception:
    pass

app = get_wsgi_application()
