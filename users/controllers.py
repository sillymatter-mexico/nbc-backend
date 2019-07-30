from core.controllers import DefaultControllers
from django.conf import settings
from django.utils import timezone
from jose import jwt
from django.core.files import File
from users.models import ClientUser, Session, StaffUser
from game.controllers import GameControllers
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
    def create_user_file(cls, cn_code):
        user = cls.get_by_id_club_premier(cn_code)
        if user is None:
            user = cls.model()
            user.club_premier_id = cn_code
            user.accepts_terms = True
            user.save()
        else:
            user.club_premier_id = cn_code
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
    def create_session(cls, user):
        number_game = 1
        game = GameControllers.search_game(number_game)
        user_session = cls.model()
        user_session.client_user_pk = user
        user_session.score = 0
        user_session.completed = False

        user_session.game = game
        user_session.high_score = 0
        user_session.level = 0
        user_session.high_bonus = 0
        user_session.bonus = 0
        user_session.score_level = 0
        user_session.bonus_level = 0
        user_session.high_score_level = 0
        user_session.high_bonus_level = 0
        user_session.attempt = 0

        user_session.save()
        return user_session

    @classmethod
    def create_session_games(cls, user, number_game):
        game = GameControllers.search_game(number_game)
        user_session = cls.model()
        user_session.client_user_pk = user
        user_session.score = 0
        user_session.completed = False

        user_session.game = game
        user_session.high_score = 0
        user_session.level = 0
        user_session.high_bonus = 0
        user_session.bonus = 0
        user_session.score_level = 0
        user_session.bonus_level = 0
        user_session.high_score_level = 0
        user_session.high_bonus_level = 0
        user_session.attempt = 0

        user_session.save()
        return user_session

    @classmethod
    def search_session(cls, uuid_user, number_game):
        session = cls.model.objects.filter(client_user_pk__uuid=uuid_user, game__order= number_game).order_by('-created')
        if session.exists():
            return session[0]
        return None

    @classmethod
    def search_session_first(cls, uuid_user):
        session = cls.model.objects.filter(client_user_pk__uuid=uuid_user).order_by('-created')
        if session.exists():
            return session[0]
        return None

    @classmethod
    def save_session(cls, user_session, data):
        user_session.completed = data['completed']

        if data['completed'] == 'True':
            if user_session.game.order == 1:
                if int(data['attempt']) == 1:
                    user_session.score = 0
                    user_session.high_score = 0
                    user_session.save()
                user_session.score = data['score']
                sum_score = user_session.high_score + int(data['score'])
                max_score = GameControllers.game(user_session.game.order)
                if sum_score >= max_score:
                    user_session.high_score = max_score
                    user_session.attempt = data['attempt']
                else:
                    user_session.high_score = sum_score
                    user_session.attempt = data['attempt']
            if user_session.game.order == 4:
                user_session.score = int(data['score'])
                max_score = GameControllers.game(user_session.game.order)
                if user_session.score < max_score:
                    if user_session.score >= user_session.high_score:
                        user_session.high_score = user_session.score
                        user_session.attempt = data['attempt']
                    else:
                        user_session.high_score = user_session.high_score
                        user_session.attempt = data['attempt']
                else:
                    user_session.high_score = max_score
                    user_session.attempt = data['attempt']
            if user_session.game.order == 2:
                if int(data['attempt']) == 1:
                    user_session.bonus = 0
                    user_session.score_level = 0
                    user_session.bonus_level = 0
                    user_session.high_score_level = 0
                    user_session.high_bonus_level = 0
                    user_session.save()
                    if int(data['level'])== 1 and int(data['attempt'])== 1:
                        user_session.high_score = 0
                        user_session.high_bonus = 0
                        user_session.save()

                user_session.level = int(data['level'])
                user_session.high_score_level = user_session.high_score_level + int(data['score'])
                user_session.high_bonus_level = user_session.high_bonus_level + int(data['bonus'])
                user_session.bonus_level = data['bonus']
                user_session.score_level = data['score']
                user_session.attempt = data['attempt']
                if int(user_session.attempt) == 3:
                    user_session.high_score = user_session.high_score + user_session.high_score_level
                    user_session.high_bonus = user_session.high_bonus + user_session.high_bonus_level
                    user_session.high_score_level = 0
                    user_session.high_bonus_level = 0
                    user_session.save()
                if int(user_session.level) == 3:
                    if int(user_session.attempt) == 3:
                        user_session.level = int(data['level'])+1
                    else:
                        user_session.level = 0
                    user_session.attempt = data['attempt']
                    user_session.score = user_session.high_score_level
                    user_session.bonus = user_session.high_bonus_level
                    sum = user_session.score + user_session.bonus
                    sum2 = user_session.high_score + user_session.high_bonus
                    if sum > sum2:
                        user_session.high_score = user_session.high_score_level
                        user_session.high_bonus = user_session.high_bonus_level
                    else:
                        user_session.high_score = user_session.high_score
                        user_session.high_bonus = user_session.high_bonus
            if user_session.game.order == 3:
                user_session.level = int(data['level'])
                user_session.high_score_level = user_session.high_score_level + int(data['score'])
                user_session.score_level = data['score']
                user_session.attempt = data['attempt']
                max_score = GameControllers.game(user_session.game.order)
                if user_session.high_score_level >= max_score:
                    user_session.high_score = max_score
                if int(user_session.level) == 3:
                    if int(user_session.attempt) == 3:
                        user_session.level = int(data['level'])+1
                    else:
                        user_session.level = 0
                    if user_session.high_score_level  >= max_score:
                        user_session.high_score = max_score
                    else:
                        if user_session.high_score_level >= user_session.high_score:
                            user_session.high_score = user_session.high_score_level
                        else:
                            user_session.high_score =user_session.high_score
                    user_session.high_score_level = 0
                    user_session.high_bonus_level = 0
        user_session.save()
        return user_session


class StaffUserControllers(DefaultControllers):
    model = StaffUser
