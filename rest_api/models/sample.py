from django.db import models


class Sample(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=1000)
    sequence = models.ForeignKey("Sequence", models.DO_NOTHING, related_name="samples")
    datahash = models.CharField(max_length=200)

    class Meta:
        db_table = "sample"


class Sample2Property(models.Model):
    property = models.OneToOneField("Property", models.DO_NOTHING, primary_key=True)
    sample = models.ForeignKey(Sample, models.DO_NOTHING)
    value_integer = models.BigIntegerField(blank=True, null=True)
    value_float = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True
    )
    value_text = models.TextField(blank=True, null=True)
    value_varchar = models.CharField(max_length=4000, blank=True, null=True)
    value_blob = models.BinaryField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    value_zip = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "sample2property"
        unique_together = (("property", "sample"),)
