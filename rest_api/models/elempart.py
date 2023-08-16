from django.db import models

from rest_api.models import Element


class Elempart(models.Model):
    id = models.BigAutoField(primary_key=True)
    element = models.OneToOneField(Element, models.DO_NOTHING)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    strand = models.BigIntegerField()
    base = models.FloatField()
    segment = models.BigIntegerField()

    class Meta:
        db_table = "elempart"
        unique_together = (("element", "segment"),)
