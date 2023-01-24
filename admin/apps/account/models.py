from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
import os
import uuid


def generate_avatar_path(instance, filename: str) -> str:
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    avatar_dir = f"users/{instance.user.username}/avatars"
    return os.path.join(avatar_dir, filename)


class UserStatus(models.Model):
    """
        User status data model.
    """
    class Meta:
        db_table = "content\".\"user_status"
        verbose_name = _("User status")
        verbose_name_plural = _("User statuses")

    status = models.CharField(
        unique=True,
        max_length=50,
        verbose_name=_("Status"),
        help_text=_("User status up to 50 characters"),
    )
    title = models.CharField(
        max_length=50,
        verbose_name=_("Description"),
        help_text=_("User status description up to 50 characters"),
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("Full description"),
        help_text=_("Status business logic"),
    )

    def __str__(self) -> CharField:
        return self.title


class UserDepartment(models.Model):
    """
        Data model of departments in the company. Filled in automatically when
        adding a new user.
    """
    class Meta:
        db_table = "content\".\"user_department"
        verbose_name = _("User division")
        verbose_name_plural = _("User divisions")

    title = models.CharField(
        max_length=150,
        verbose_name=_("User department"),
        help_text=_("Brief title of the structure in the company"),
    )
    block = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("Block"),
        help_text=_("Block name in the company"),
    )
    department = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("Departament"),
        help_text=_("Departament name in the company"),
    )
    group = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Group"),
        help_text=_("Group name in the company"),
    )
    branch = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Branch"),
        help_text=_("Branch name in the company"),
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Description name in the company"),
    )

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
        The user profile data model. Profile is created automatically when
        creating a new user in the system. Communication with the User model
        :model: `auth.User`.
    """
    class Meta:
        db_table = "content\".\"user_profile"
        verbose_name = _("User profile")
        verbose_name_plural = _("Users profiles")
        ordering = ["last_name"]
        unique_together = (
            ("user", "last_name"),
            ("user", "uuid"),
        )
        get_latest_by = "created_time"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("User UUID"),
        help_text=_("Filled in automatically by the system"),
    )
    status = models.ForeignKey(
        UserStatus,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=1,
        related_name="user_status",
        verbose_name=_("The user's status in the system"),
    )
    avatar = models.ImageField(
        default="system/user-dummy-img.jpg",
        upload_to=generate_avatar_path,
    )
    last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("User last name"),
        help_text=_("Up to 50 characters"),
    )
    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("User first name"),
        help_text=_("Up to 50 characters"),
    )
    middle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("User middle name"),
        help_text=_("Up to 50 characters"),
    )
    mobile_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_("User mobile phone number"),
        help_text=_("Primary contact number"),
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_("User phone number"),
        help_text=_("Any phone number"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("User profile description"),
        help_text=_("Additional Information"),
    )
    department = models.ForeignKey(
        UserDepartment,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_department",
        verbose_name=_("User department in the company"),
    )
    experience_start = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Experience start date"),
    )
    experience_now = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Experience end date"),
    )
    experience_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Experience description"),
    )
    post = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("User post"),
        help_text=_("User post in the company"),
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("User info created time"),
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name=_("User info updated time"),
    )

    def shot_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def abbreviation(self) -> str:
        name = ""
        patronymic = ""
        if self.first_name:
            name = self.first_name[0]
        if self.middle_name:
            patronymic = self.middle_name[0]
        return f"{self.last_name} {name}.{patronymic}."

    def show_mobile_phone(self) -> str:
        return PhoneNumber.from_string(
            phone_number=self.mobile_phone,
            region=settings.PHONE_NUMBERS_REGION,
        ).as_e164

    def show_phone(self) -> str:
        return PhoneNumber.from_string(
            phone_number=self.phone,
            region=settings.PHONE_NUMBERS_REGION,
        ).as_e164

    def __str__(self) -> str:
        return self.full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
