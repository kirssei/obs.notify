from django.urls import path

from .views import (
    TwitchLogin,
    TwitchCallbackLogin,
    TwitchNotifyFollowDebugView,
    LoginView,
    LogoutView,
    SyncRewardsView,
    SaveRewardsView,
    MainPageView,
)

urlpatterns = [
    path("twitch/login/", TwitchLogin.as_view(), name="twitch_login"),
    path("twitch/callback/", TwitchCallbackLogin.as_view(), name="twitch_callback"),
    path(
        "debug/follow",
        TwitchNotifyFollowDebugView.as_view(),
        name="twitch-debug-follow",
    ),
    path("login", LoginView.as_view(), name="auth"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("sync-rewards", SyncRewardsView.as_view(), name="sync-rewards"),
    path("save-rewards", SaveRewardsView.as_view(), name="save-rewards"),
    path("", MainPageView.as_view(), name="main-page"),
]
