from core.view_rest import NoTokenView
from users.controllers import ClientUserControllers
from users.serializers import ClientUserSerializer
from users.forms import LoginForm

class Login(NoTokenView):
    def post(self, request):
        login_form = LoginForm(request.data)
        if not login_form.is_valid():
            return self.api_fail_response(
                None, 'ID incorrecto')
        data = request.data
        id_club_premier = data['club_premier_id']
        accepts_terms = data['accepts_terms']
        if accepts_terms == 'False':
            message = 'Debe aceptar los Terminos'
            return self.api_fail_response({}, message)
        status = ClientUserControllers.id_validate(id_club_premier)
        if not status:
            return self.api_fail_response(
                None, 'ID incorrecto')
        user = ClientUserControllers.get_by_id_club_premier(id_club_premier)
        if user is None:
            user = ClientUserControllers.create_user(data)
        user_data = ClientUserSerializer(user, many=False).data
        token = ClientUserControllers.create_token(user)
        user_data['token'] = token
        messages = 'Bienvenido'
        return self.api_ok_response(user_data, messages)
