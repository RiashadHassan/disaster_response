from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModelWithUID

User = get_user_model()


class Division(BaseModelWithUID):
    name = models.CharField(max_length=255)
    bengali_name = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=20, decimal_places=15, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=20, decimal_places=15, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Name {self.name}"


class District(BaseModelWithUID):
    name = models.CharField(max_length=255)
    bengali_name = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=20, decimal_places=15, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=20, decimal_places=15, null=True, blank=True
    )

    # Relationship
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Name {self.name}"


class Upazila(BaseModelWithUID):
    """
    this is also police station
    """

    # Relationship Important
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    # General Information
    name = models.CharField(max_length=255)
    bengali_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Name {self.name}"

    class Meta:
        unique_together = ("name", "district", "division")


class PostOffice(BaseModelWithUID):
    # Relationship Important
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, null=True, blank=True
    )
    upazila = models.ForeignKey(
        Upazila, on_delete=models.CASCADE, null=True, blank=True
    )

    # General Information
    name = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Name {self.name}"


class Address(BaseModelWithUID):
    # General Information
    country = models.CharField(
        verbose_name="Country name", max_length=255, blank=True, default="Bangladesh"
    )
    house_street = models.CharField(
        verbose_name="House and street", max_length=255, blank=True
    )
    label = models.CharField(max_length=255, blank=True)

    # Relationship ForeignKey
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )
    upazila = models.ForeignKey(
        Upazila, on_delete=models.SET_NULL, null=True, blank=True
    )
    post_office = models.ForeignKey(
        PostOffice, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - UID: {self.uid}, Country {self.country}"


class AddressConnector(BaseModelWithUID):
    # Relationship Important
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    # Relationship ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    disaster = models.ForeignKey(
        "disaster.DisasterEvent", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        unique_together = ("address", "user")

    def __str__(self):
        return f"{self.id} - UID: {self.uid}"
