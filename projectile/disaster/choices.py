from django.db import models


class DisasterEventStatusChoices(models.TextChoices):
    REPORTED = "reported", "REPORTED"
    IN_PROGRESS = "in_progress", "IN_PROGRESS"
    CONFIRMED = "confirmed", "CONFIRMED"
    RESOLVED = "resolved", "RESOLVED"


class DisasterEventRiskChoices(models.TextChoices):
    UNKNOWN = "unknown", "UNKNOWN"
    LOW = "low", "LOW"
    MODERATE = "moderate", "MODERATE"
    HIGH = "high", "HIGH"
    UTMOST = "utmost", "UTMOST"
