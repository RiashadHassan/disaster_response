from django.db import models


class MediaKindChoices(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"
    ASSESSMENT = "ASSESSMENT", "Assessment"
    ATTACHED_FILE = "ATTACHED_FILE", "Attached File"
