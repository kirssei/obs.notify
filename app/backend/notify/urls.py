from django.urls import path

from .views import TwitchLogin, TwitchCallbackLogin, TwitchNotifyFollowDebugView

urlpatterns = [
    path("login/", TwitchLogin.as_view(), name="twitch_login"),
    path("callback/", TwitchCallbackLogin.as_view(), name="twitch_callback"),
    path("debug/follow", TwitchNotifyFollowDebugView.as_view(), name="twitch-debug-follow")

]
