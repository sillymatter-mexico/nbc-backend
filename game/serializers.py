from rest_framework import serializers
from game.models import Game, Label


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'order', 'uuid')


class LabelSerializer(serializers.ModelSerializer):
    game_pk = GameSerializer(many=False, read_only=True)
    class Meta:
        model = Label
        fields = ('name', 'order', 'game_pk', 'uuid')
