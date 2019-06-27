from rest_framework import serializers
from game.models import Game, Label


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'order', 'total_levels', 'uuid')


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'order', 'game_pk', 'uuid')
