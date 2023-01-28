import os
import pytest

from django.conf import settings
from django.utils.version import get_version
from config.settings import INSTALLED_APPS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = "admin"
MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
if (PROJECT_DIR_NAME not in root_dir_content or not os.path.isdir(MANAGE_PATH)):
    assert False, (
        f"In directory `{BASE_DIR}` not found folder with "
        f"project `{PROJECT_DIR_NAME}`. "
        f"Make sure you have the correct project structure."
    )

project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = "manage.py"
if FILENAME not in project_dir_content:
    assert False, (
        f"In directory `{MANAGE_PATH}` not found file `{FILENAME}`. "
        f"Make sure you have the correct project structure."
    )

assert get_version() < "4.0.0", "Please use version Django < 4.0.0"

assert any(app in INSTALLED_APPS for app in [
    "phonenumber_field",
    "apps.account"
]), (
    "Please register the application at `settings.INSTALLED_APPS`"
)


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "test_scc_db",
        "NAME": "test_scc_db",
        "PASSWORD": "Qinsjhgvv45LJSD",
        "USER": "test_scc_user",
        "PORT": 5433,
    }


pytest_plugins = [
    "tests.fixtures.fixture_user",
    "tests.fixtures.fixture_data",
]
