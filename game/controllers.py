from core.controllers import DefaultControllers
from game.models import Game, Label


class GameControllers(DefaultControllers):
    model = Game


class LabelControllers(DefaultControllers):
    model = Label
    @classmethod
    def search_game_first(cls, number_game):
        session = cls.model.objects.filter(game_pk__order=number_game, order='1')
        return session[0]

    @classmethod
    def search_next_label(cls, num, order_game):
        label= cls.model.objects.filter(game_pk__order=order_game, order=num, game_pk__enable=True)
        if label.exists():
            return label[0]
        return None
