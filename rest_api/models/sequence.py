from django.db import models


class Sequence(models.Model):
    id = models.BigAutoField(primary_key=True)
    seqhash = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = "sequence"
