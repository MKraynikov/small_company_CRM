import tempfile

import pytest
from mixer.backend.django import mixer as _mixer
from apps.account.models import UserStatus


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture(scope="session")
def user_status(user):
    return UserStatus.objects.create(
        status="Test status",
        title="Test status title",
        imadescriptionge="Test status description"
    )
