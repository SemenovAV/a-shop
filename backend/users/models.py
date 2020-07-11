#!/usr/bin/env python3
from __future__ import annotations

from typing import Any
from typing import Dict

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import gettext as _


class CustomUserManager(UserManager):
    def _create_user(
        self: CustomUserManager,
        username: str,
        email: str,
        password: str,
        **extra_fields: Dict[str, Any],
    ) -> Any:
        """
        Create and save a user with the given username, email, and password.
        """
        superuser_group = Group.objects.get(name="administrators")
        user = super().create_user(username, email, password, **extra_fields)

        if extra_fields.get("is_superuser"):
            user = super().create_superuser(username, email, password, **extra_fields)
            superuser_group.user_set.add(user)  # type: ignore

        return user


class CustomUser(AbstractUser):
    objects = CustomUserManager()


class CustomGroup(Group):
    is_staff: models.BooleanField = models.BooleanField(
        default=False, verbose_name=_("staff status"),
    )
