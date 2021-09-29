from json.decoder import JSONDecoder
import uuid
import json
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    face_encoding = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)