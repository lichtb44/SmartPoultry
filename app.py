"""
Render fallback WSGI entrypoint.

Some Render services default to `gunicorn app:app`. The Django project lives in
the `smartpoultry` subdirectory, so this module exposes the Django WSGI
application under that expected name.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR / "smartpoultry"

sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

