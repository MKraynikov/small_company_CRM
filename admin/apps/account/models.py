from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        Модель данных статусов пользователей.
    """
    class Meta:
        db_table = "content\".\"user_status"
        verbose_name = "Статус пользователя"
        verbose_name_plural = "Статусы пользователей"

    status = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="Статус",
        help_text="Статус пользователя до 50 символов",
    )
    title = models.CharField(
        max_length=50,
        verbose_name="Описание",
        help_text="Описание статуса пользователя до 50 символов",
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Полное описание",
        help_text="Бизнес логика статуса.",
    )

    def __str__(self) -> str:
        return self.title


class UserDepartment(models.Model):
    """
        Модель данных отделов в компании. Заполняется автоматически при
        добавлении нового пользователя.
    """
    class Meta:
        db_table = "content\".\"user_department"
        verbose_name = "Подразделение пользователя"
        verbose_name_plural = "Подразделения пользователей"

    title = models.CharField(
        max_length=150,
        verbose_name="Заголовок",
        help_text="Краткий заголовок структуры в компании",
    )
    block = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Блок",
        help_text="Название блока в компании",
    )
    department = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Департамент",
        help_text="Название департамента в компании",
    )
    group = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Отдел",
        help_text="Название отдела в компании",
    )
    branch = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Группа",
        help_text="Название группы в компании",
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Описание структуры в компании",
    )

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
        Модель данных профилей пользователя. Профиль создается автоматически
        при создании нового пользователя в системе. Связь с моделью User
        :model: `auth.User`.
    """
    class Meta:
        db_table = "content\".\"user_profile"
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
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
        verbose_name="UUID пользователя",
        help_text="Заполняется автоматически системой.",
    )
    status = models.ForeignKey(
        UserStatus,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=1,
        related_name="user_status",
        verbose_name="Статус пользователя в системе.",
    )
    avatar = models.ImageField(
        default="system/user-dummy-img.jpg",
        upload_to=generate_avatar_path,
    )
    last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Фамилия пользователя",
        help_text="До 50 символов.",
    )
    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Имя пользователя",
        help_text="До 50 символов.",
    )
    middle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Отчество пользователя",
        help_text="До 50 символов.",
    )
    mobile_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Номер мобильного телефона",
        help_text="Основной контактный номер.",
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Номер телефона",
        help_text="Любой номер телефона.",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Примечание к профилю",
        help_text="Дополнительная информация",
    )
    department = models.ForeignKey(
        UserDepartment,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_department",
        verbose_name="Отдел пользователя в компании",
    )
    experience_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала работы",
    )
    experience_now = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания работы.",
    )
    experience_description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Обязанности.",
    )
    post = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Должность",
        help_text="Должность пользователя.",
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Время создания",
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Время изменения",
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
            phone_number=self.mobile_phone, region="RU",
        ).as_e164

    def show_phone(self) -> str:
        return PhoneNumber.from_string(
            phone_number=self.phone, region="RU",
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
