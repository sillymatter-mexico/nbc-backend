from core.controllers import DefaultControllers
from game.models import Game


class GameControllers(DefaultControllers):
    model = Game
    @classmethod
    def search_game(cls, number_game):
        session = cls.model.objects.filter(order=number_game)
        return session[0]

    @classmethod
    def game(cls, number_game):
        game =  cls.model.objects.filter(order=number_game)
        game = game[0].max_score
        return game
