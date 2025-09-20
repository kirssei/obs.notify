from django.contrib import admin

from .models import TwitchRedem


@admin.register(TwitchRedem)
class TwitchRedemAdmin(admin.ModelAdmin):
    list_display = ("user", "reward", "text", "created_at")
    