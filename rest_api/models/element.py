from django.db import models


class Element(models.Model):
    id = models.BigAutoField(primary_key=True)
    molecule = models.ForeignKey("Molecule", models.DO_NOTHING)
    type = models.CharField(max_length=100)
    accession = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    description = models.TextField()
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    strand = models.BigIntegerField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    standard = models.BigIntegerField()
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = "element"
