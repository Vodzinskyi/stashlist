import uuid

from django.db import models
from django.contrib.auth.models import User

from apps.media_items.models import MediaItem

class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MediaItem)

    def __str__(self):
        return self.name
