import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
password = 'Admin123!'
email = 'admin@example.com'
if User.objects.filter(username=username).exists():
    print('EXISTS')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('CREATED')
print('USERNAME=' + username)
print('PASSWORD=' + password)
