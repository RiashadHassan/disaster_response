from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from shared.base_model import BaseModelWithUID

from .choices import GenderChoices
from .managers import CustomUserManager
from .utils import get_slug_full_name


class User(AbstractBaseUser, PermissionsMixin, BaseModelWithUID):
    # General Information
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    slug = AutoSlugField(populate_from=get_slug_full_name, editable=False, unique=True)

    phone = PhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=20, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN
    )
    location = models.CharField(max_length=200, blank=True, null=True)

    # Relationship ForeignKey
    address = models.ForeignKey(
        "addressio.Address", on_delete=models.CASCADE, null=True, blank=True
    )

    media_files = models.ManyToManyField(
        "mediaroom.MediaRoom", through="mediaroom.MediaRoomConnector", blank=True
    )

    # additional settings for User
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    # Managers
    objects = CustomUserManager()

    def __str__(self):
        name = " ".join([self.first_name, self.last_name])
        data = (
            f"Name: {name}, Email: {self.email}"
            if len(self.email) > 0
            else f"Name: {name} Phone: {self.phone}"
        )

        return f"{self.id} - UID: {self.uid}, {data}"

    def get_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        name = f"{self.first_name} {self.last_name}"
        return name.strip()

    def media_files(self):
        return self.media_files.filter()
