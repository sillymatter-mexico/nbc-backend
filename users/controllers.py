from core.controllers import DefaultControllers
from django.conf import settings
from django.utils import timezone
from jose import jwt
from django.core.files import File
from users.models import ClientUser, Session, StaffUser


class ClientUserControllers(DefaultControllers):
    model = ClientUser

    @classmethod
    def create_user(cls, data):
        user = cls.model()
        user.club_premier_id = data['club_premier_id']
        user.accepts_terms = True
        user.save()
        return

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
        print('hl')
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


class SessionControllers(DefaultControllers):
    model = Session


class StaffUserControllers(DefaultControllers):
    model = StaffUser
