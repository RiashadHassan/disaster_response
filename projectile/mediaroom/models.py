from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModelWithUID

from .choices import MediaKindChoices

from disaster.models import DisasterEvent
from response.models import Response, Aftermath

User = get_user_model()


# Create your models here.
class MediaRoom(BaseModelWithUID):
    # image
    image = models.ImageField(
        width_field="width",
        height_field="height",
        null=True,
        blank=True,
    )
    title = models.CharField(blank=True, max_length=500)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    # General Information
    file = models.FileField(null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=MediaKindChoices.choices, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Type: {self.type}"


class MediaRoomConnector(BaseModelWithUID):
    # Relationship Important
    media_room = models.ForeignKey("mediaroom.MediaRoom", on_delete=models.CASCADE)

    # General Information
    type = models.CharField(max_length=50, choices=MediaKindChoices.choices)

    # Relationship ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    disaster_event = models.ForeignKey(
        DisasterEvent, on_delete=models.CASCADE, null=True, blank=True
    )
    response = models.ForeignKey(
        Response, on_delete=models.CASCADE, null=True, blank=True
    )
    aftermath = models.ForeignKey(
        Aftermath, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Type: {self.type}"
