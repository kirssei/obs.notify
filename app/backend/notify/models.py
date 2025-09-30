from django.db import models


class TwitchBaseReward(models.Model):
    reward_id = models.CharField(verbose_name="Reward ID", max_length=255)
    name = models.CharField(verbose_name="Name", max_length=255)
    cost = models.CharField(verbose_name="Cost", max_length=255)
    is_enabled = models.BooleanField(verbose_name="Is enabled", default=False)
    use_tts = models.BooleanField(verbose_name="User TTS", default=False)

    def __str__(self):
        return self.reward_id

    @classmethod
    def get_by_reward_id(cls, reward_id):
        return cls.objects.filter(reward_id=reward_id).last()


class TwitchReward(models.Model):
    user = models.CharField(verbose_name="Nickname", max_length=255)
    reward = models.CharField(verbose_name="Reward", max_length=255)
    text = models.TextField(
        verbose_name="Text",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.reward}"


class TwitchFollow(models.Model):
    user = models.CharField(verbose_name="Nickname", max_length=255)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    def __init__(self):
        return self.user


class TwitchSecretsApp(models.Model):
    client_id = models.CharField(verbose_name="Client ID", max_length=255)
    client_secret = models.CharField(verbose_name="Client Secret", max_length=255)
    is_valid = models.BooleanField(verbose_name="Is valid?", default=False)

    @classmethod
    def get_secrets(cls):
        return cls.objects.last()

    @classmethod
    def save_secrets(cls, client_id, client_secret):
        obj, _ = cls.objects.update_or_create(
            id=1,
            defaults={"client_id": client_id, "client_secret": client_secret},
        )

        return obj

    def __str__(self):
        return "TwitchSecrets"


class TwitchTokens(models.Model):
    access_token = models.CharField(verbose_name="Access token", max_length=255)
    refresh_token = models.CharField(verbose_name="Refresh token", max_length=255)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    @classmethod
    def get_tokens(cls):
        return cls.objects.last()

    @classmethod
    def save_tokens(cls, access_token, refresh_token):
        obj, _ = cls.objects.update_or_create(
            id=1,
            defaults={"access_token": access_token, "refresh_token": refresh_token},
        )
        return obj

    def __str__(self):
        return "TwitchTokens"
