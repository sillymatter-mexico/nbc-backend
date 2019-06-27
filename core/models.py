import uuid as uuid_lib

from django.db import models

# Create your models here.


def uuid_hex():
    return uuid_lib.uuid4().hex


class DatableModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class PublicModel(DatableModel):
    uuid = models.CharField(db_index=True, max_length=32, default=uuid_hex,
                            unique=True, editable=False)
    enable = models.BooleanField(default=True)

    class Meta:
        abstract = True
