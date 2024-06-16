from django.db import models
from shared.base_model import BaseModelWithUID


class DisasterEvent(BaseModelWithUID):
    event_id = models.AutoField(primary_key=True)
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    severity = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.event_type
