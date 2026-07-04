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
RUNNING_ON_RENDER = bool(os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_HOSTNAME"))

sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

if RUNNING_ON_RENDER and os.getenv("SMARTPOULTRY_SKIP_STARTUP_TASKS") != "1":
    import django
    from django.core.management import call_command

    django.setup()
    call_command("migrate", interactive=False, verbosity=1)
    call_command("collectstatic", interactive=False, verbosity=0)

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
