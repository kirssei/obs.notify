from django.db import models


class TwitchRedem(models.Model):
    user = models.CharField(verbose_name="Ник", max_length=255)
    reward = models.CharField(verbose_name="Награда", max_length=255)
    text = models.TextField(
        verbose_name="Текст",
        help_text="Пустое, если награда не предполагает ввода текста",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name="Дата получения", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.reward}"

    class Meta:
        verbose_name = ("Награда зрителя",)
        verbose_name_plural = "Награды зрителей"


class TwitchTokens(models.Model):
    access_token = models.CharField(verbose_name="Токен доступа", max_length=255)
    refresh_token = models.CharField(verbose_name="Докен обновления", max_length=255)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

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
