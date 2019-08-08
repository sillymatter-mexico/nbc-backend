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
        #user = ClientUser.objects.filter(club_premier_id=client_user)
        #a=int(user[0].accumulation)*10
        return Session.objects.filter(client_user_pk=client_user).aggregate(Sum('high_score')).get('high_score__sum')
    def get_completed_game(self, client_user):
        session_list = Session.objects.filter(client_user_pk=client_user)
        cont = 0
        for session in session_list:
            id_game=session.game.id
            if id_game ==2 or id_game==3:
                if session.high_score != 0:
                    cont = cont+1
            else:
                max_score= Game.objects.filter(id=id_game)[0].max_score
                high_score= session.high_score
                if high_score == max_score or session.attempt == 3:
                    cont = cont+1
        return cont
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
