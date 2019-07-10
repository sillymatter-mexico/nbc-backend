from django.urls import path, include, re_path
from users.api_view import Login, General_information, Create_session, Save_session

api_url = [
    re_path('^login/$', Login.as_view(), name='Login'),
    re_path('^(?P<client_user_uuid>[0-9a-f]{32})/info/$', General_information.as_view(), name='Info'),
    re_path('^(?P<client_user_uuid>[0-9a-f]{32})/session/$', Create_session.as_view(), name='Info'),
    re_path('^(?P<client_user_uuid>[0-9a-f]{32})/save_session/$', Save_session.as_view(), name='Info'),
]

urlpatterns = [
    path('', include(api_url)),
]
