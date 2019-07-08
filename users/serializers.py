from rest_framework import serializers
from users.models import ClientUser, Session, StaffUser
from game.serializers import LabelSerializer


class ClientUserSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    class Meta:
        model = ClientUser
        fields = ('club_premier_id', 'uuid')
    def get_total_score(self, client_user):
        return Session.objects.filter(client_user_pk=client_user)

class SessionSerializer(serializers.ModelSerializer):
    client_user_pk = ClientUserSerializer(many=False, read_only=True)
    label = LabelSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ('client_user_pk', 'score', 'label', 'attempt', 'completed', 'uuid')


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ('first_name', 'last_name', ' email', 'password', 'uuid')
