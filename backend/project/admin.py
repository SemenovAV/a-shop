#!/usr/bin/env python3
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy


class MyAdminSite(admin.AdminSite):

    site_title = gettext_lazy("Shop admin")
    site_header = gettext_lazy("Shop administration")
    index_title = gettext_lazy("Administration")

    def has_permission(self: MyAdminSite, request: object) -> bool:
        return (
            request.user.is_active
            and request.user.groups.filter(group__is_staff=True).exists()
        )


site = MyAdminSite()
admin.site = site
admin.sites.site = site
