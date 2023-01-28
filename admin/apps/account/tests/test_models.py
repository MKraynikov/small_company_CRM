from django.test import TestCase
from apps.account.models import UserStatus


class UserStatusModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_status = UserStatus.objects.create(
            status="Q" * 100,
            title="Z" * 100,
            description="User status description"
        )

    def test_status_max_length_not_exceed(self):
        status = UserStatusModelTest.status
        max_length_status = status._meta.get_field("status").max_length
        length_slug = len(status.status)
        self.assertEqual(max_length_status, length_slug)
