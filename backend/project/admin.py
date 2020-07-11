#!/usr/bin/env python3
from __future__ import annotations

from typing import cast

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils.translation import gettext_lazy

CustomUser = get_user_model()


class MyAdminSite(admin.AdminSite):

    site_title = gettext_lazy("Shop admin")
    site_header = gettext_lazy("Shop administration")
    index_title = gettext_lazy("Administration")

    def has_permission(self: MyAdminSite, request: HttpRequest) -> bool:
        user = cast(User, request.user)
        return user.is_active and user.groups.filter(group__is_staff=True).exists()


admin.site = MyAdminSite()
