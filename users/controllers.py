from core.controllers import DefaultControllers
from django.conf import settings
from django.utils import timezone
from jose import jwt
from django.core.files import File
from users.models import ClientUser, Session, StaffUser
from game.controllers import GameControllers, LabelControllers
from luhn import *


class ClientUserControllers(DefaultControllers):
    model = ClientUser

    @classmethod
    def create_user(cls, data):
        user = cls.model()
        user.club_premier_id = data['club_premier_id']
        user.accepts_terms = True
        user.save()
        return user

    @classmethod
    def get_by_token(cls, token):
        """Trae el token del usuario"""
        try:
            data = jwt.decode(token, settings.SECRET_KEY, 'HS256')
            return data
        except:
            return None

    @classmethod
    def create_token(cls, user_obj):
        """Crea Token cada que se hace login"""
        try:
            return jwt.encode(
                dict(uuid=user_obj.uuid,
                     passwordToken=user_obj.passwordToken.hex,
                     data=timezone.now().strftime('%Y-%m-%d %H:%M:%SZ')),
                settings.SECRET_KEY, 'HS256'
            )
        except:
            return None

    @classmethod
    def id_validate(cls, id_club_premier):
        validation=verify(id_club_premier)
        if validation is True:
            return True
        return False

class SessionControllers(DefaultControllers):
    model = Session

    @classmethod
    def create_session(cls, user, number_game):
        label= LabelControllers.search_game_first(number_game)
        user_session = cls.model()
        user_session.client_user_pk = user
        user_session.score = '0'
        user_session.completed = False
        user_session.attempt = '1'
        user_session.label = label
        user_session.save()
        return user_session

    @classmethod
    def search_session(cls, uuid_user):
        session = cls.model.objects.filter(client_user_pk__uuid=uuid_user).order_by('-created')
        if session.exists():
            session=session[0]
            return session
        return None

    @classmethod
    def next_session(cls, user_session):
        next_session= cls.model()
        next_session.completed = False
        next_session.score = 0
        next_session.client_user_pk= user_session.client_user_pk
        if user_session.attempt == 3: #numero de intentos
            if user_session.label.order != 3: #numero de niveles
                u=user_session.label.order+1
                order_game= user_session.label.game_pk.order
                label= LabelControllers.search_next_label(u, order_game)
                next_session.label = label
                next_session.attempt = 1
                next_session.save()
                return next_session

            order_game = user_session.label.game_pk.order+1
            label=1
            a = LabelControllers.search_next_label(label, order_game)
            if a is None:
                return None
            next_session.label= a
            next_session.attempt = 1
            next_session.save()
            return next_session
        next_session.label = user_session.label
        next_session.attempt = user_session.attempt +1
        next_session.save()
        return next_session

    @classmethod
    def save_session(cls, user_session, data):
        user_session.score = data['score']
        user_session.completed = data['completed']

        if data['completed']=='True':
            next_session = SessionControllers.next_session(user_session)
            if next_session is None:
                user_session.save()
                return None
           # user_session.attempt=user_session.attempt+1

        user_session.save()
        return user_session

class StaffUserControllers(DefaultControllers):
    model = StaffUser
