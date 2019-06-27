from django.urls import path, include, re_path
from users.api_view import Login

api_url = [
    re_path('^login/$', Login.as_view(), name='Login'),
]

urlpatterns = [
    path('', include(api_url)),
]
