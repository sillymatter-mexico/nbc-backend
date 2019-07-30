from rest_framework import serializers
from users.models import ClientUser, Session, StaffUser
from game.models import Game
from game.serializers import GameSerializer
from django.db.models import Sum

class SessionGameSerializer(serializers.ModelSerializer):
    game = GameSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ('game', 'attempt', 'completed', 'uuid', 'level',  'score_level', 'bonus_level', 'high_score_level', 'high_bonus_level', 'bonus', 'score', 'high_bonus','high_score')


class ClientUserSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    game = serializers.SerializerMethodField()
    completed_game = serializers.SerializerMethodField()


    class Meta:
        model = ClientUser
        fields = ('club_premier_id', 'uuid', 'completed_game','accumulation',  'total_score', 'game')
    def get_total_score(self, client_user):
        user = ClientUser.objects.filter(club_premier_id=client_user)
        a=int(user[0].accumulation)*10
        return Session.objects.filter(client_user_pk=client_user).aggregate(Sum('high_score')).get('high_score__sum')+a
    def get_completed_game(self, client_user):
        return Session.objects.filter(client_user_pk=client_user, attempt=3).count()
    def get_game(self, client_user):
        return SessionGameSerializer(client_user.session_set.all(), many=True).data

class SessionSerializer(serializers.ModelSerializer):
    client_user_pk = ClientUserSerializer(many=False, read_only=True)
    game = GameSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ('client_user_pk', 'game', 'attempt', 'completed', 'uuid', 'level',  'score_level', 'bonus_level', 'high_score_level', 'high_bonus_level', 'bonus', 'score', 'high_bonus','high_score')

class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ('first_name', 'last_name', ' email', 'password', 'uuid')
