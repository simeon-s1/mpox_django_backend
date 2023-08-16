from django.db import models


class Reference(models.Model):
    id = models.BigAutoField(primary_key=True)
    accession = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    organism = models.CharField(max_length=100, blank=True, null=True)
    translation = models.ForeignKey("Translation", models.DO_NOTHING)
    standard = models.BigIntegerField()

    class Meta:
        db_table = "reference"
