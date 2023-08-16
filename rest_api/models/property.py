from django.db import models


class Property(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    datatype = models.CharField(max_length=45)
    querytype = models.CharField(max_length=45)
    description = models.TextField()
    target = models.CharField(max_length=45)
    standard = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = "property"
