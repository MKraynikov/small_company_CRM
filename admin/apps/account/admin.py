from django.contrib import admin
from apps.account.models import UserStatus, UserDepartment, UserProfile
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "title",
        "description",
    )
    list_display_links = (
        "id",
        "status",
    )
    search_fields = (
        "status",
        "title",
        "description",
    )
    empty_value_display = _("-not filled-")


class UserDepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "block",
        "department",
        "group",
        "branch",
    )
    list_display_links = (
        "id",
        "department",
    )
    search_fields = (
        "title",
        "block",
        "department",
        "group",
        "branch",
    )
    empty_value_display = _("-not filled-")


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "last_name",
        "first_name",
        "middle_name",
        "status",
        "mobile_phone",
        "department",
        "post",
    )
    list_display_links = (
        "user",
        "last_name",
    )
    list_editable = (
        "status",
        "department",
    )
    ordering = (
        "last_name",
        "first_name",
    )
    search_fields = (
        "user",
        "last_name",
        "first_name",
        "middle_name",
        "status",
        "department",
    )
    readonly_fields = (
        "user_link",
    )
    list_filter = (
        "status",
        "post",
        "department",
    )
    empty_value_display = _("-not filled-")

    def user_link(self, obj):
        return mark_safe("<a href='{}'>{}</a>".format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            obj.user.username
        ))

    user_link.short_description = "user"


admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(UserDepartment, UserDepartmentAdmin)
admin.site.register(UserProfile, UserAdmin)
