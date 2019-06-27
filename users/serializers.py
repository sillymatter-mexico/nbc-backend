from rest_framework import serializers
from users.models import ClientUser, Session, StaffUser


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('club_premier_id', 'uuid')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        field = ('client_user_pk', 'score', 'completed', 'uuid')


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        field = ('first_name', 'last_name', ' email', 'password', 'uuid')
