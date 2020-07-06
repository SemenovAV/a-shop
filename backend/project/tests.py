#!/usr/bin/env python3
import os

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.test import SimpleTestCase
from django.test import TestCase
from django.test.client import Client
from project.admin import MyAdminSite


class TestProject(SimpleTestCase):
    @classmethod
    def setUpClass(cls: SimpleTestCase) -> None:
        cls.test_title = "Test Title"
        MyAdminSite.site_title = cls.test_title
        super().setUpClass()

    @classmethod
    def test_admin(cls: SimpleTestCase) -> None:
        assert admin.site.site_title == cls.test_title

    @classmethod
    def test_apps(cls: SimpleTestCase) -> None:
        assert AdminConfig.name == "django.contrib.admin"
        assert apps.get_app_config("admin").name == "django.contrib.admin"

    @classmethod
    def test_asgi(cls: SimpleTestCase) -> None:
        assert os.environ["DJANGO_SETTINGS_MODULE"] == "backend.project.settings"

    @classmethod
    def test_urls(cls: SimpleTestCase) -> None:
        c = Client()
        admin_response = c.get("/admin/")
        login_response = c.get("/admin/login/")
        assert admin_response.status_code == 302
        assert login_response.status_code == 200


class TestProjectWithDB(TestCase):
    @classmethod
    def test_urls(cls: TestCase) -> None:
        c = Client()
        login_response = c.post(
            "/admin/login/", {"username": "admin", "password": "admin",},
        )
        assert login_response.status_code == 200
