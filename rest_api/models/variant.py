from django.db import models

from rest_api.models import Element, Property


class ExcludeAltNManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(alt="N")


class Variant(models.Model):
    id = models.BigAutoField(primary_key=True)
    element = models.ForeignKey(Element, models.DO_NOTHING)
    pre_ref = models.CharField(max_length=1, blank=True, null=True)
    ref = models.CharField(max_length=200)
    alt = models.CharField(max_length=200)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    parent_id = models.BigIntegerField(blank=True, null=True)
    label = models.TextField()
    frameshift = models.BigIntegerField()
    alignment = models.ManyToManyField(
        "Variant", through="Alignment2Variant", related_name="variants"
    )
    objects = ExcludeAltNManager()

    class Meta:
        db_table = "variant"
        unique_together = (("element", "start", "end", "ref", "alt"),)


class Variant2Property(models.Model):
    property = models.OneToOneField(Property, models.DO_NOTHING, primary_key=True)
    variant = models.ForeignKey(Variant, models.DO_NOTHING)
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
        db_table = "variant2property"
        unique_together = (("property", "variant"),)


class Variant2Annotation(models.Model):
    variant = models.OneToOneField("Variant", models.DO_NOTHING, primary_key=True)
    alignment = models.ForeignKey("Alignment", models.DO_NOTHING)
    annotation = models.ForeignKey("AnnotationType", models.DO_NOTHING)

    class Meta:
        db_table = "variant2annotation"
        unique_together = (("variant", "alignment", "annotation"),)
