from django.urls import path, include


urlpatterns = [path("notify/", include("app.backend.notify.urls"))]
