#!/usr/bin/env python3
from django.contrib import admin
from django.utils.translation import gettext_lazy


class MyAdminSite(admin.AdminSite):

    site_title = gettext_lazy("Shop admin")
    site_header = gettext_lazy("Shop administration")
    index_title = gettext_lazy("Administration")


admin.site = MyAdminSite()
