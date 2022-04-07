from users.models import User


def user_get_all() -> list:
    users = User.objects.all()
    return [user_get_access(user=u) for u in users]


def user_get_refresh(*, user: User):
    return {"email": user.email, "refresh_token": user.refresh_token}


def user_get_access(*, user: User):
    return {"email": user.email, "access_token": user.access_token}


def user_get_detail(*, user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "team_name": user.team.name,
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "me": user_get_detail(user=user),
    }
