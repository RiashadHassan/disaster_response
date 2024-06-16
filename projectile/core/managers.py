from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValidationError(_("Email address is required"))
        if not password:
            raise ValidationError(_("Password is required"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.first_name = first_name.title()
        user.last_name = last_name.title()
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        return user
