from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.forms import MyUserChangeForm
from users.models import CustomUser
from users.models import Group


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active", "groups"),}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    @classmethod
    def save_model(
        cls: MyUserAdmin,
        request: object,
        obj: CustomUser,
        form: MyUserChangeForm,
        change: bool,
    ) -> None:
        if change:
            obj.is_staff = form.cleaned_data["groups"].filter(is_staff=True).exists()
            obj.save()
            super().save_model(request, obj, form, change)


class MyGroupAdmin(GroupAdmin):
    list_display = ("name", "is_staff")

    @classmethod
    def save_model(
        cls: MyGroupAdmin, request: object, obj: Group, form: object, change: bool,
    ) -> None:
        if change:
            for user in obj.user_set.all():
                if (
                    obj.is_staff is False
                    and not user.groups.filter(is_staff=True)
                    .exclude(pk=obj.pk)
                    .exists()
                ):
                    user.is_staff = False
                    user.save()
                else:
                    user.is_staff = True
                    user.save()
            super().save_model(request, obj, form, change)


admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Group, MyGroupAdmin)
