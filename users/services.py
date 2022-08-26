from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key
from config import settings

from utils import get_now

from datetime import datetime
from datetime import timedelta

from users.models import Team, User


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
    user.first_name = extra_data["first_name"]
    user.last_name = extra_data["last_name"]
    user.access_token = extra_data["access_token"]
    user.refresh_token = extra_data["refresh_token"]
    user.picture = extra_data["picture"]
    user.team = extra_data["team"]
    user.full_clean()
    user.save()

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


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True


@transaction.atomic
def team_get_or_create(*, name: str, **extra_data) -> Tuple[Team, bool]:
    team = Team.objects.filter(name=name).first()
    if team:
        return team, False
    return team_create(name=name, **extra_data), True


@transaction.atomic
def team_create(*, name: str, **extra_fields) -> Team:
    import stripe

    stripe.api_key = settings.STRIPE_API_KEY
    customer = stripe.Customer.create(
        description=f"Stripe customer representing Google organization {name}",
        name=name,
        email=extra_fields["owner_email"],
    )
    today = datetime.now()
    # Trial ends 14 from now
    trial_end = int((today + timedelta(days=14)).timestamp())
    # Billing start the last day of current month
    billing_cycle_anchor = int(
        (
            today.replace(month=today.month + 2).replace(day=1) - timedelta(days=1)
        ).timestamp()
    )
    subscription = stripe.Subscription.create(
        customer=customer.stripe_id,
        items=[
            {"price": settings.STRIPE_DEFAULT_PRICING, "quantity": 0},
        ],
        trial_end=trial_end,
        billing_cycle_anchor=billing_cycle_anchor,
    )
    team = Team(
        name=name,
        owner_email=extra_fields["owner_email"],
        stripe_customer_id=customer.stripe_id,
        stripe_subscription_id=subscription.stripe_id,
    )
    team.full_clean()
    team.save()

    return team
