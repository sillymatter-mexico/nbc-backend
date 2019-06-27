from core.controllers import DefaultControllers
from game.models import Game, Label


class GameControllers(DefaultControllers):
    model = Game


class LabelControllers(DefaultControllers):
    model = Label
