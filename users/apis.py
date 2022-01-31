from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from api.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin

from auth.services import (
    google_get_access_token_from_refresh,
    google_get_user_info,
    jwt_login,
    google_validate_id_token,
)
from users.models import User

from users.services import user_update_access_token, user_get_or_create
from users.selectors import user_get_me


class UserMeApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.user.email).first()
        try:
            google_get_user_info(access_token=user.access_token)
        except ValidationError:
            # TODO: Handle exception if refresh fail
            new_access_token = google_get_access_token_from_refresh(
                refresh_token=user.refresh_token
            )
            user_update_access_token(user=user, new_access_token=new_access_token)

        return Response(user_get_me(user=user))


class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False, default="")
        last_name = serializers.CharField(required=False, default="")

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get("Authorization")
        google_validate_id_token(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        response = Response(data=user_get_me(user=user))
        response = jwt_login(response=response, user=user)

        return response
