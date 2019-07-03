from django.urls import path, include, re_path
from game.api_view import Show_games

api_url = [
    re_path('^show_games/$', Show_games.as_view(), name='Login'),
]

urlpatterns = [
    path('', include(api_url)),
]
