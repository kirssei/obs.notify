from django.urls import path

from .views import TwitchLogin, TwitchCallbackLogin

urlpatterns = [
    path("login/", TwitchLogin.as_view(), name="twitch_login"),
    path("callback/", TwitchCallbackLogin.as_view(), name="twitch_callback"),
]
