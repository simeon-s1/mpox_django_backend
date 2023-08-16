from django.db import models


class Molecule(models.Model):
    id = models.BigAutoField(primary_key=True)
    reference = models.ForeignKey("Reference", models.DO_NOTHING)
    type = models.CharField(max_length=100)
    accession = models.CharField(unique=True, max_length=100)
    symbol = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    length = models.BigIntegerField()
    segment = models.BigIntegerField()
    standard = models.BigIntegerField()

    class Meta:
        db_table = "molecule"
