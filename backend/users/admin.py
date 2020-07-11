#!/usr/bin/env python3
from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Set
from typing import Tuple

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .forms import MyUserChangeForm
from .models import CustomGroup
from .models import CustomUser


class MyUserAdmin(UserAdmin):
    list_displayL: Tuple = ("username", "is_staff")
    form: Callable[[Any, Any], MyUserChangeForm] = MyUserChangeForm
    fieldsets: Tuple = (
        (None, {"fields": ("username", "password", "groups")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active",),}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_form(
        self: MyUserAdmin,
        request: HttpRequest,
        obj: None = None,
        change: bool = False,
        **kwargs: Dict[str, Any],
    ) -> Any:
        user = cast(CustomUser, request.user)
        form: Any = super().get_form(request, obj, change, **kwargs)
        is_superuser: bool = user.is_superuser
        disabled_fields: Set[str] = set()
        if not is_superuser:
            disabled_fields |= {
                "username",
                "is_superuser",
                "user_permissions",
                "is_active",
                "groups",
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def save_model(
        self: MyUserAdmin,
        request: HttpRequest,
        obj: CustomUser,
        form: MyUserChangeForm,
        change: bool,
    ) -> None:
        data = form.cleaned_data.get("groups")
        if data:
            obj.is_staff = data.filter(group__is_staff=True).exists()

        super().save_model(request, obj, form, change)


class MyGroupAdmin(GroupAdmin):
    list_display = ("name", "is_staff")
    fieldsets = ((None, {"fields": ("name", "is_staff", "permissions")}),)

    def save_model(
        self: MyGroupAdmin,
        request: HttpRequest,
        obj: CustomGroup,
        form: object,
        change: bool,
    ) -> None:
        super().save_model(request, obj, form, change)
        for user in obj.user_set.all():  # type: ignore
            if (
                obj.is_staff is False
                and not user.groups.filter(groups__is_staff=True)
                .exclude(pk=obj.pk)
                .exists()
            ):
                user.is_staff = False
                user.save()
            else:
                user.is_staff = True
                user.save()


admin.site.unregister(Group)
admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(CustomGroup, MyGroupAdmin)
