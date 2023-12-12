from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"leaderboard/", consumers.LeaderboardConsumer.as_asgi()),
]

