from django.contrib.auth.models import User


def create_user(
    username='test',
    password='12345',
):
    return User.objects.create_user(
        username=username,
        password=password,
    )
