from django.db import models


class Lineages(models.Model):
    id = models.BigAutoField(primary_key=True)
    lineage = models.CharField(max_length=100)
    sublineage = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "lineages"
