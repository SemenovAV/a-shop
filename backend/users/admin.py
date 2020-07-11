#!/usr/bin/env python3
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.forms import MyUserChangeForm
from users.models import Group
from users.models import User


class MyUserAdmin(UserAdmin):
    list_display = ("username", "is_staff")
    form = MyUserChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password", "groups")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active",),}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    @classmethod
    def save_model(
        cls: MyUserAdmin,
        request: object,
        obj: User,
        form: MyUserChangeForm,
        change: bool,
    ) -> None:
        data = form.cleaned_data.get("groups")
        if data:
            obj.is_staff = data.filter(group__is_staff=True).exists()

        super().save_model(
            cls, request, obj, form, change,
        )


class MyGroupAdmin(GroupAdmin):
    list_display = ("name", "is_staff")
    fieldsets = ((None, {"fields": ("name", "is_staff", "permissions")}),)

    @classmethod
    def save_model(
        cls: MyGroupAdmin, request: object, obj: Group, form: object, change: bool,
    ) -> None:
        super().save_model(
            cls, request, obj, form, change,
        )
        for user in obj.user_set.all():
            if (
                obj.customgroup.is_staff is False
                and not user.groups.filter(groups__is_staff=True)
                .exclude(pk=obj.pk)
                .exists()
            ):
                user.is_staff = False
                user.save()
            else:
                user.is_staff = True
                user.save()


admin.site.register(User, MyUserAdmin)
admin.site.register(Group, MyGroupAdmin)
