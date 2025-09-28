import asyncio
from asgiref.sync import async_to_sync

from django.views import View
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect

from .models import TwitchTokens
from .auth import TwitchOAuthClient

from app.asgi import handler

class TwitchLogin(View):

    def get(self, request, *args, **kwargs):
        oauth_client = TwitchOAuthClient(
            settings.TWITCH_CLIENT_ID,
            settings.TWITCH_CLIENT_SECRET,
            settings.TWITCH_REDIRECT_URI,
        )
        url = oauth_client.get_login_url(settings.TWITCH_SCOPES)
        return HttpResponseRedirect(url)


class TwitchCallbackLogin(View):

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "no code"}, status=400)
        oauth_client = TwitchOAuthClient(
            settings.TWITCH_CLIENT_ID,
            settings.TWITCH_CLIENT_SECRET,
            settings.TWITCH_REDIRECT_URI,
        )
        tokens = asyncio.run(oauth_client.fetch_token(code))
        TwitchTokens.save_tokens(
            access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]
        )
        return JsonResponse(tokens)

class TwitchNotifyFollowDebugView(View):

    def get(self, request, *args, **kwargs):
        async_to_sync(handler.simulate_subscription)("TestUser")
        return JsonResponse({"status": "ok", "user": "TestUser"})
