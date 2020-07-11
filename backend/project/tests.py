#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import Type

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.test import SimpleTestCase
from django.test import TestCase
from django.test.client import Client

from .admin import MyAdminSite


class TestProject(SimpleTestCase):
    test_title = None

    @classmethod
    def setUpClass(cls: Type[TestProject]) -> None:
        cls.test_title = "Test Title"
        MyAdminSite.site_title = cls.test_title
        super().setUpClass()

    def test_admin(self: TestProject) -> None:
        assert admin.site.site_title == self.test_title

    def test_apps(self: TestProject) -> None:
        assert AdminConfig.name == "django.contrib.admin"
        assert apps.get_app_config("admin").name == "django.contrib.admin"

    def test_asgi(self: TestProject) -> None:
        assert os.environ["DJANGO_SETTINGS_MODULE"] == "backend.project.settings"

    def test_urls(self: TestProject) -> None:
        c = Client()
        admin_response = c.get("/admin/")
        login_response = c.get("/admin/login/")
        assert admin_response.status_code == 302
        assert login_response.status_code == 200


class TestProjectWithDB(TestCase):
    fixtures = ["backend/fixture.json"]

    def test_urls_login(self: TestProjectWithDB) -> None:
        c = Client()
        login_response = c.post(
            "/admin/login/", {"username": "admin", "password": "admin",},
        )
        assert login_response.status_code == 302
        assert login_response.url == "/accounts/profile/"

    def test_urls_false_login(self: TestProjectWithDB) -> None:
        c = Client()
        login_response = c.post(
            "/admin/login/", {"username": "user", "password": "admin",},
        )
        assert login_response.status_code == 200
