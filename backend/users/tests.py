#!/usr/bin/env python3
from __future__ import annotations

from django.apps import apps
from django.test import SimpleTestCase
from django.test import TestCase

from .apps import UsersConfig
from .models import Group


class TestApp(SimpleTestCase):
    def test_apps(self: TestApp) -> None:
        assert UsersConfig.name == "users"
        assert apps.get_app_config("users").name == "users"


class TestAppWithDB(TestCase):
    fixtures = ["backend/fixture.json"]

    @classmethod
    def setUpTestData(cls: TestAppWithDB) -> None:
        cls.group_name = "test_group"
        Group.objects.create(name=cls.group_name, is_staff=True)

    def test_group_model_is_staff_label(self: TestAppWithDB) -> None:
        group = Group.objects.get(id=1)
        label = group._meta.get_field("is_staff").verbose_name

        assert label == "staff status"
