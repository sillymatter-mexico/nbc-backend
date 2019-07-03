from core.view_rest import NoTokenView, TokenView
from users.controllers import ClientUserControllers, SessionControllers
from users.serializers import ClientUserSerializer, SessionSerializer
from users.forms import LoginForm

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
    def get(self, request):
        user_id = self.user.club_premier_id
        user = ClientUserControllers.get_by_id_club_premier(user_id)
        user_data = ClientUserSerializer(user, many=False).data
        return self.api_ok_response(user_data, '')

class Create_session(TokenView):
    def post(self, request):

        user_id = self.user.club_premier_id
        data = request.data
        number_game = data['number_game']

        user = ClientUserControllers.get_by_id_club_premier(user_id)
        session_user =SessionControllers.search_session(user.uuid)
        if session_user is None:
            session_user = SessionControllers.create_session(user, number_game)
        info = SessionSerializer(session_user, many=False).data
        return self.api_fail_response(info, '')


class Save_session(TokenView):
    def post(self, request, client_user_uuid):
        data= request.data
        client_user= ClientUserControllers.get_by_uuid(client_user_uuid)
        number_game = data['number_game']
        session_user =SessionControllers.search_session(client_user.uuid)
        save_session = SessionControllers.save_session(session_user, data)
        if save_session is None:
            message="Juegos y niveles finalizados"
            return self.api_ok_response({}, message)
        info = SessionSerializer(session_user, many=False).data
        return self.api_fail_response(info, '')