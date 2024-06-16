from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from shared.base_model import BaseModelWithUID

from .choices import UserStatus, GenderChoices
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
    is_verified = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        db_index=True,
        default=UserStatus.ACTIVE,
    )

    # Relationship ManyToManyField
    addresses = models.ManyToManyField(
        "addressio.Address", through="addressio.AddressConnector", blank=True
    )
    media_files = models.ManyToManyField(
        "mediaroomio.MediaRoom", through="mediaroomio.MediaRoomConnector", blank=True
    )

    skills = models.ManyToManyField(
        "candidateio.Skill",
        through="candidateio.SkillConnector",
        blank=True,
    )
    # General information
    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=20, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    remote_address = models.CharField(max_length=200, blank=True, null=True)
    website = models.JSONField(default=dict, null=True, blank=True)

    # Relationship ForeignKey
    address = models.ForeignKey(
        "addressio.Address", on_delete=models.CASCADE, null=True, blank=True
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

    def activate(self):
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()

    def removed(self):
        self.status = UserStatus.REMOVED
        self.save_dirty_fields()

    def check_if_user_has_role(self, role: str) -> bool:
        return self.organizationuser_set.filter(role=role).exists()

    def __str__(self):
        return f"{self.id} - UID: {self.uid}"

    def media_files(self):
        return self.user.media_files.filter()
