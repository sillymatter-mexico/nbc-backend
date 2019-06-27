from django.urls import path, include

urlpatterns = [
    path('users/', include('users.url_api')),
    #path('game/', include('game.url_api')),
]
