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
    accumulation = models.IntegerField(null=True, blank=True, verbose_name=u'Acumulación Premier')

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
    bonus = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)
    high_bonus = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)
    level = models.IntegerField(blank=True, null=True)
    score_level = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)
    bonus_level = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)
    high_score_level = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)
    high_bonus_level = models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)

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


class ReportUsers(PublicModel):
    name = models.CharField(max_length=125,
                            verbose_name=u'Nombre del Archivo')
    start_date = models.DateField(verbose_name=u'Fecha de inicio',
                                  help_text=u'Fecha desde donde iniciara el '
                                            u'reporte')
    finish_date = models.DateField(verbose_name=u'Fecha de fin',
                                   help_text=u'Fecha hasta donde llegara el'
                                             u' reporte')
    email = models.EmailField()
    url = models.FileField(upload_to="report/punctuation/", blank=True,
                           help_text=u'Después de terminado el reporte se '
                                     u'podra descargar desde esta URL')
    percent = models.SmallIntegerField(default=0, blank=True, verbose_name=u'Porcentaje Genera Total')
    percent_report = models.SmallIntegerField(default=0, blank=True, verbose_name=u'Porcentaje Reporte')


class UpdateFile(PublicModel):
    file = models.FileField(upload_to='file/database')
    percent = models.SmallIntegerField(default=0, blank=True)

    def __str__(self):
        return '{0} %'.format(self.percent)