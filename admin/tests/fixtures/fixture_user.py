import pytest


@pytest.fixture(scope="session")
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        password='1234567'
    )


@pytest.fixture(scope="session")
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture(scope="session")
def another_user(mixer):
    from django.contrib.auth.models import User
    return mixer.blend(User, username='AnotherUser')
