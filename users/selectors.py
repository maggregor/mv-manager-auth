from users.models import User


def user_get_me(*, user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "first_name": user.first_name,
        "access_token": user.access_token,
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "me": user_get_me(user=user),
    }
