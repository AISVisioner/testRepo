import uuid
# from django.conf import settings
from django.db import models
# from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # encoding = ArrayField(models.FloatField)
    photo = models.ImageField(blank=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    recent_access_at = models.DateTimeField(auto_now=True, editable=False)