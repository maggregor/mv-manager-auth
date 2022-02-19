from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key

from utils import get_now

from users.models import User


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_get(email) -> User:
    user = User.objects.filter(email=email).first()
    return user


def user_update(user: User, **extra_data) -> User:
    user = user_update_access_token(
        user=user, new_access_token=extra_data["access_token"]
    )
    user = user_update_refresh_token(
        user=user, new_refresh_token=extra_data["refresh_token"]
    )
    user = user_update_name(
        user=user,
        new_first_name=extra_data["first_name"],
        new_last_name=extra_data["last_name"],
    )

    return user

@transaction.atomic
def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

    user = user_create(email=email, password=password, **extra_fields)

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_update_access_token(*, user: User, new_access_token: str) -> User:
    user.access_token = new_access_token
    user.full_clean()
    user.save()

    return user


def user_update_refresh_token(*, user: User, new_refresh_token: str) -> User:
    user.refresh_token = new_refresh_token
    user.full_clean()
    user.save()

    return user


def user_update_name(*, user: User, new_first_name: str, new_last_name: str) -> User:
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True
