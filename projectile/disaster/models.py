from django.db import models
from shared.base_model import BaseModelWithUID

from .choices import DisasterEventStatusChoices, DisasterEventRiskChoices
from core.models import User
from core.utils import get_event_id


class DisasterEvent(BaseModelWithUID):

    event_id = models.CharField(blank=True, null=True, editable=False)
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ended_on = models.DateTimeField(null=True, blank=True)

    # severity of the event, not risk to human lives
    severity_level = models.FloatField(default=None, null=True, blank=True)
    description = models.TextField(default="not yet provided", blank=True)

    status = models.CharField(
        max_length=50,
        choices=DisasterEventStatusChoices,
        default=DisasterEventStatusChoices.REPORTED,
    )

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    affected_population = models.IntegerField(blank=True, null=True)
    damage_cost = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    emergency_response_units = models.TextField(blank=True, null=True)
    additional_resources_needed = models.TextField(blank=True, null=True)

    media_files = models.ManyToManyField(
        "mediaroom.MediaRoom", through="mediaroom.MediaRoomConnector", blank=True
    )

    reporters = models.ManyToManyField(
        "core.User", through="disaster.DisasterEventConnector", blank=True
    )

    relief_centers = models.TextField(blank=True, null=True)

    # risk to human lives
    risk_level = models.CharField(
        max_length=50,
        choices=DisasterEventRiskChoices,
        default=DisasterEventRiskChoices.UNKNOWN,
        blank=True,
    )

    def __str__(self):
        return f"{self.event_type} - {self.location} - {self.date.strftime('%Y-%m-%d')}"


class DisasterEventConnector(BaseModelWithUID):

    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    disaster_event = models.ForeignKey(DisasterEvent, on_delete=models.CASCADE)
