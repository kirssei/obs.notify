import asyncio
import logging
from asgiref.sync import sync_to_async

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope
from twitchAPI.eventsub.websocket import EventSubWebsocket

from django.conf import settings
from .models import (
    TwitchReward,
    TwitchTokens,
    TwitchSecretsApp,
    TwitchFollow,
    TwitchBaseReward,
)
from .websocket import WebSocketBroadcaster
from .utils import generate_tts

logger = logging.getLogger(__name__)


class TwitchEventHandler:
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.twitch: Twitch | None = None
        self.eventsub: EventSubWebsocket | None = None
        self.user = None
        self.broadcaster = WebSocketBroadcaster()

    async def setup(self) -> bool:
        tokens = await sync_to_async(TwitchTokens.get_tokens)()
        if not tokens:
            return False

        secrets = await sync_to_async(TwitchSecretsApp.get_secrets)()
        if not secrets:
            return False

        self.twitch = await Twitch(secrets.client_id, secrets.client_secret)

        scopes = [
            AuthScope.MODERATOR_READ_FOLLOWERS,
            AuthScope.CHANNEL_READ_REDEMPTIONS,
        ]

        await self.twitch.set_user_authentication(
            token=tokens.access_token, scope=scopes, refresh_token=tokens.refresh_token
        )

        self.user = await first(self.twitch.get_users(logins=[self.channel_name]))

        from twitchAPI.eventsub.websocket import EventSubWebsocket

        self.eventsub = EventSubWebsocket(self.twitch)
        self.eventsub.start()

        await self.register_events()

        return True

    async def sync_rewards(self):
        if not self.user or not self.twitch:
            return []

        rewards = await self.twitch.get_custom_reward(broadcaster_id=self.user.id)

        for reward in rewards:
            await sync_to_async(TwitchBaseReward.objects.update_or_create)(
                reward_id=reward.id,
                defaults={
                    "name": reward.title,
                    "cost": reward.cost,
                    "is_enabled": reward.is_enabled,
                },
            )

        return rewards

    async def simulate_subscription(self, username="[Debug] TestUser"):
        await sync_to_async(lambda: TwitchFollow.objects.create(user=username))()
        await self.broadcaster.broadcast("follow", {"user": username})

    async def register_events(self):
        await self.eventsub.listen_channel_follow_v2(
            self.user.id, self.user.id, self.on_follow
        )
        await self.eventsub.listen_channel_points_custom_reward_redemption_add(
            self.user.id, self.on_redemption
        )

    async def on_follow(self, data):
        username = data.event.user_name
        await sync_to_async(lambda: TwitchFollow.objects.create(user=username))()
        await self.broadcaster.broadcast("follow", {"user": username})

    async def on_redemption(self, data):
        user = data.event.user_name
        reward = data.event.reward.title
        reward_id = data.event.reward.id
        message = data.event.user_input

        await sync_to_async(
            lambda: TwitchReward.objects.create(user=user, reward=reward, text=message)
        )()

        base_reward = await sync_to_async(
            lambda: TwitchBaseReward.get_by_reward_id(reward_id=reward_id)
        )()

        if base_reward.use_tts:
            tts_file = generate_tts(text=message)

            await self.broadcaster.broadcast(
                "reward",
                {
                    "user": user,
                    "reward": reward,
                    "message": message,
                    "tts_url": tts_file,
                },
            )

        else:
            await self.broadcaster.broadcast(
                "reward", {"user": user, "reward": reward, "message": message}
            )

    async def run_forever(self):
        while True:
            started = await self.setup()
            if started:
                break
            await asyncio.sleep(10)

        try:
            while True:
                await asyncio.sleep(3600)
        except Exception as e:
            logger.exception("Error in TwitchEventHandler: %s", e)
        finally:
            if self.eventsub:
                await self.eventsub.stop()
            if self.twitch:
                await self.twitch.close()
