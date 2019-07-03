from core.view_rest import NoTokenView, TokenView
from game.controllers import GameControllers
from game.serializers import GameSerializer

class Show_games(TokenView):
    def post(self, request):
        games = GameControllers.get_all()
        info = GameSerializer(games, many=True).data
        return self.api_ok_response(info, '')