#!/usr/bin/env python3
from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    default_site = "project.admin.MyAdminSite"