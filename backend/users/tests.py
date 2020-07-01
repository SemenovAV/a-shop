from __future__ import annotations

from django.apps import apps
from django.test import TestCase

from backend.users.apps import UsersConfig


class TestApp(TestCase):
    def test_apps(self: TestApp) -> None:
        assert UsersConfig.name == "users"
        assert apps.get_app_config("users").name == "backend.users"
