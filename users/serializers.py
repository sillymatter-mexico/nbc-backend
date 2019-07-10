from rest_framework import serializers
from users.models import ClientUser, Session, StaffUser
from game.serializers import GameSerializer
from django.db.models import Sum

class ClientUserSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    class Meta:
        model = ClientUser
        fields = ('club_premier_id', 'uuid', 'total_score')
    def get_total_score(self, client_user):
        return Session.objects.filter(client_user_pk=client_user).aggregate(Sum('high_score'))



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
