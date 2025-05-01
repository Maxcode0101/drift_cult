import os
from django.conf import settings

def file_exists_locally(path):
    return os.path.isfile(os.path.join(settings.MEDIA_ROOT, path))