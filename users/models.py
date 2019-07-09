from django.db import models
from core.models import PublicModel, uuid_hex
import uuid

# Create your models here.


class ClientUser(PublicModel):
    club_premier_id = models.CharField(max_length=45, null=True, blank=True,
                                       verbose_name=u'ID Club Premier')
    accepts_terms = models.BooleanField(default=False, verbose_name=u'Terminos')
    passwordToken = models.UUIDField(default=uuid.uuid4, editable=False,
                                     unique=True)

    def __str__(self):
        return '{0}'.format(self.club_premier_id)


class Session(PublicModel):
    client_user_pk = models.ForeignKey(ClientUser, models.SET_NULL, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                blank=True)
    label = models.ForeignKey('game.Label', models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField()
    attempt = models.IntegerField(null=True, blank=True)
    game = models.ForeignKey('game.Game', models.SET_NULL, null=True, blank=True)
    high_score = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                blank=True)
    def __str__(self):
        return '{0}{1}{2}'.format(self.client_user_pk, self.score,
                                  self.completed)


class StaffUser(PublicModel):
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return '{0}{1}{2}'.format(self.first_name, self.last_name, self.email)
