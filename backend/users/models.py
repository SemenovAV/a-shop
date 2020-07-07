from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    pass


class Group(Group):

    is_staff = models.BooleanField(default=False, verbose_name=_("staff status"))
