from django.db import models
from core.models import PublicModel
# Create your models here.


class Game(PublicModel):
    name = models.CharField(max_length=45, null=True, blank=True,
                            verbose_name=u'Nombre')
    order = models.IntegerField(null=True, blank=True)
    total_levels = models.IntegerField(null=True, blank=True)
    max_score = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                blank=True)

    def __str__(self):
        return '{0}{1}{2}'.format(self.order, self.order, self.total_levels)


class Label(PublicModel):
    name = models.CharField(max_length=45, null=True, blank=True,
                            verbose_name=u'Nombre')
    order = models.IntegerField(null=True, blank=True)
    game_pk = models.ForeignKey(Game, models.SET_NULL, null=True)

    def __str__(self):
        return '{0}{1}'.format(self.order, self.game_pk)
