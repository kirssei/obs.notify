from django.db import models


class TwitchRedem(models.Model):
    user = models.CharField(
        verbose_name="Ник",
        max_length=255
    )
    reward = models.CharField(
        verbose_name="Награда",
        max_length=255
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Пустое, если награда не предполагает ввода текста",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name="Дата получения",
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.reward}"

    class Meta:
        verbose_name = "Награда зрителя",
        verbose_name_plural = "Награды зрителей"