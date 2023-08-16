from django.db import models


class Translation(models.Model):
    id = models.BigAutoField(primary_key=True)
    codon = models.CharField(max_length=100)
    aa = models.CharField(max_length=100)

    class Meta:
        db_table = "translation"
