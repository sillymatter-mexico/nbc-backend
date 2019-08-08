from core.view_rest import NoTokenView, TokenView
from users.controllers import ClientUserControllers, SessionControllers
from users.serializers import ClientUserSerializer, SessionSerializer
from users.forms import LoginForm
from game.controllers import GameControllers

class Login(NoTokenView):
    def post(self, request):
        login_form = LoginForm(request.data)
        if not login_form.is_valid():
            return self.api_fail_response(
                None, 'ID incorrecto')
        data = request.data
        id_club_premier = data['club_premier_id']
        status = ClientUserControllers.id_validate(id_club_premier)
        if not status:
            return self.api_fail_response(
                None, 'ID incorrecto')
        user = ClientUserControllers.get_by_id_club_premier(id_club_premier)
        if user is None:
            accepts_terms = data['accepts_terms']
            if accepts_terms == 'False':
                message = 'Debe aceptar los Terminos'
                return self.api_fail_response({}, message)
            user = ClientUserControllers.create_user(data)
       # user_session = SessionControllers.create_session(user)
        user_data = ClientUserSerializer(user, many=False).data
        token = ClientUserControllers.create_token(user)
        user_data['token'] = token
        messages = 'Bienvenido'
        return self.api_ok_response(user_data, messages)

class General_information(TokenView):
    def get(self, request, client_user_uuid):
        client_user = ClientUserControllers.get_by_uuid(client_user_uuid)
        user = ClientUserControllers.get_by_id_club_premier(client_user)
        user_data = ClientUserSerializer(user, many=False).data
        return self.api_ok_response(user_data, '')

class Create_session(TokenView):
    def post(self, request, client_user_uuid):
        client_user = ClientUserControllers.get_by_uuid(client_user_uuid)
        data = request.data
        number_game = int(data['number_game'])
        session_user = SessionControllers.search_session_first(client_user.uuid)
        if session_user is None:
            session_user = SessionControllers.create_session(client_user)
        if session_user.game.order > number_game:
            session_user = SessionControllers.search_session(client_user_uuid, number_game)
            if session_user.game.order == 2 or session_user.game.order == 3:
                session_user = SessionControllers.search_session(client_user_uuid, number_game)
                if session_user.attempt == 4:
                    messages = "juego finalizado"
                    return self.api_fail_response({}, messages)
                else:
                    info = SessionSerializer(session_user, many=False).data
                    return self.api_ok_response(info, '')
            messages = "Jugar finalizado"
            return self.api_fail_response({}, messages)
        if session_user.game.order < number_game:
            number_session = session_user.game.order + 1
            if number_session == number_game:
                if session_user.game.order == 2 or session_user.game.order == 3:
                    previous_session = int(number_game) - 1
                    a=SessionControllers.search_session(client_user_uuid, previous_session)
                    if a is None:
                        messages = "Jugar en orden"
                        return self.api_fail_response({}, messages)
                    if a.high_score != 0:
                        session_user = SessionControllers.create_session_games(
                            client_user, number_game)
                        info = SessionSerializer(session_user, many=False).data
                        return self.api_ok_response(info, '')
                    if a.high_score == 0:
                        messages = "Jugar en orden"
                        return self.api_fail_response({}, messages)
                max_score = GameControllers.game(session_user.game.order)
                if session_user.attempt == 3 or session_user.high_score >= max_score:
                    session_user = SessionControllers.create_session_games(client_user, number_game)
                    info = SessionSerializer(session_user, many=False).data
                    return self.api_ok_response(info, '')
            messages = "Jugar en orden"
            return self.api_fail_response({}, messages)
        if number_game == session_user.game.order:
            max_score = GameControllers.game(number_game)
            if session_user.game.order == 2 or session_user.game.order==3:
                if session_user.attempt == 4:
                    messages = "juego finalizado"
                    return self.api_fail_response({}, messages)
                info = SessionSerializer(session_user, many=False).data
                return self.api_ok_response(info, '')
            if session_user.attempt == 3 or session_user.high_score >= max_score:
                messages = "Juego finalizado"
                return self.api_fail_response({}, messages)
        info = SessionSerializer(session_user, many=False).data
        return self.api_ok_response(info, '')


class Save_session(TokenView):
    def post(self, request, client_user_uuid):
        data = request.data
        number_game = data['number_game']
        session_user = SessionControllers.search_session(client_user_uuid, number_game)
        max_score = GameControllers.game(number_game)
        if int(number_game) == 2 or int(number_game) == 3:
            if session_user.attempt == 3 or session_user.attempt == 4 or session_user.high_score >= max_score:
                message = "Juego finalizado"
                return self.api_ok_response({}, message)
        else:
            if session_user.attempt == 3 or session_user.high_score >= max_score:
                message = "Juego finalizado"
                return self.api_ok_response({}, message)
        save_session = SessionControllers.save_session(session_user, data)
        info = SessionSerializer(save_session, many=False).data
        return self.api_ok_response(info, '')
