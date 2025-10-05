import asyncio
from asgiref.sync import async_to_sync

from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect

from .models import (
    TwitchTokens,
    TwitchReward,
    TwitchFollow,
    TwitchSecretsApp,
    TwitchBaseReward,
)
from .auth import TwitchOAuthClient

from app.asgi import handler


class TwitchLogin(View):
    def get(self, request, *args, **kwargs):
        client_id = request.GET.get("client_id")
        client_secret = request.GET.get("client_secret")

        obj, _ = TwitchSecretsApp.objects.update_or_create(
            id=1, defaults={"client_id": client_id, "client_secret": client_secret}
        )

        oauth_client = TwitchOAuthClient(
            obj.client_id,
            obj.client_secret,
            settings.TWITCH_REDIRECT_URI,
        )
        url = oauth_client.get_login_url(settings.TWITCH_SCOPES)

        return HttpResponseRedirect(url)


class TwitchCallbackLogin(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "no code"}, status=400)

        secrets = TwitchSecretsApp.objects.last()

        oauth_client = TwitchOAuthClient(
            secrets.client_id,
            secrets.client_secret,
            settings.TWITCH_REDIRECT_URI,
        )
        tokens = async_to_sync(oauth_client.fetch_token)(code=code)
        try:
            TwitchTokens.save_tokens(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
            )

            secrets.is_valid = True
            secrets.save()

        except KeyError:
            return JsonResponse({"error": "no access_token"}, status=400)
        return HttpResponseRedirect("/notify/")


class LoginView(View):
    template_name = "notify/templates/auth.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")

        return HttpResponseRedirect(
            f"/notify/twitch/login?client_id={client_id}&client_secret={client_secret}"
        )


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        TwitchSecretsApp.objects.all().delete()
        return HttpResponseRedirect("/notify/login")


class SaveRewardsView(View):
    def post(self, request, *args, **kwargs):
        for reward in TwitchBaseReward.objects.all():
            use_tts = request.POST.get(f"tts_{reward.id}") == "on"
            reward.use_tts = use_tts
            reward.save()
        return HttpResponseRedirect("/notify/")


class SyncRewardsView(View):
    def post(self, request, *args, **kwargs):
        async_to_sync(handler.sync_rewards)()
        return HttpResponseRedirect("/notify/")


class MainPageView(View):
    template_name = "notify/templates/index.html"

    def get(self, request, *args, **kwargs):
        reward_list = TwitchReward.objects.all().order_by("-created_at")
        follow_list = TwitchFollow.objects.all().order_by("-created_at")
        base_rewards = TwitchBaseReward.objects.filter(is_enabled=True)
        secrets = TwitchSecretsApp.objects.filter(is_valid=True).last()

        auth = bool(secrets)
        if not auth:
            return HttpResponseRedirect("/notify/login")

        reward_page_number = request.GET.get("reward_page", 1)
        follow_page_number = request.GET.get("follow_page", 1)

        reward_paginator = Paginator(reward_list, 8)
        follow_paginator = Paginator(follow_list, 60)

        rewards = reward_paginator.get_page(reward_page_number)
        follows = follow_paginator.get_page(follow_page_number)

        context = {"base_rewards": base_rewards, "follows": follows, "rewards": rewards}

        return render(request, self.template_name, context)


class TwitchNotifyFollowDebugView(View):
    def get(self, request, *args, **kwargs):
        async_to_sync(handler.simulate_subscription)("TestUser")
        return JsonResponse({"status": "ok", "user": "TestUser"})
