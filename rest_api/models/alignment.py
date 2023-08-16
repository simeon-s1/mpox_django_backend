from django.db import models


class Alignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    sequence = models.ForeignKey("Sequence", models.DO_NOTHING, null=True)
    element = models.ForeignKey("Element", models.DO_NOTHING)
    variant = models.ManyToManyField(
        "Variant", through="Alignment2Variant", related_name="alignments"
    )

    class Meta:
        db_table = "alignment"
        unique_together = (("sequence", "element"),)



class Alignment2Variant(models.Model):
    alignment = models.ForeignKey(Alignment, models.DO_NOTHING)
    variant = models.OneToOneField("Variant", models.DO_NOTHING, primary_key=True)

    class Meta:
        db_table = "alignment2variant"
        unique_together = (("variant", "alignment"),)
