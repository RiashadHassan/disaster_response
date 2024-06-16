import uuid

from django.db import models

from dirtyfields import DirtyFieldsMixin
from django.utils import timezone


class BaseModelWithUID(DirtyFieldsMixin, models.Model):
    class Meta:
        abstract = True

    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
