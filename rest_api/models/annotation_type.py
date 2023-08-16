from django.db import models


class AnnotationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    seq_ontology = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    test = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "annotation_type"
