from django.urls import path

from users.apis import UserListApi, UserMeApi, UserInitApi, UserAccessTokenApi


urlpatterns = [
    path("me/", UserMeApi.as_view(), name="me"),
    path("init/", UserInitApi.as_view(), name="init"),
    path("/", UserListApi.as_view(), name="all"),
    path("/", UserAccessTokenApi.as_view(), name="access-token"),
]
