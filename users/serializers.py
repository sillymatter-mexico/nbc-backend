from rest_framework import serializers
from users.models import ClientUser, Session, StaffUser
from game.serializers import LabelSerializer, GameSerializer


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('club_premier_id', 'uuid')


class SessionSerializer(serializers.ModelSerializer):
    client_user_pk = ClientUserSerializer(many=False, read_only=True)
    game = GameSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ('client_user_pk', 'score', 'high_score', 'game', 'attempt', 'completed', 'uuid')


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ('first_name', 'last_name', ' email', 'password', 'uuid')
