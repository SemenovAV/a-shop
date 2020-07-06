from __future__ import annotations

from django.apps import apps
from django.test import SimpleTestCase

from backend.users.apps import UsersConfig


class TestApp(SimpleTestCase):
    def test_apps(self: TestApp) -> None:
        assert UsersConfig.name == "users"
        assert apps.get_app_config("users").name == "users"
