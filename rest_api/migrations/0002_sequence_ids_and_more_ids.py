# Generated by Django 4.1.6 on 2023-08-09 12:50

from django.db import migrations, models
import django.db.models.deletion


def insert_seqhash_ids(apps, schema_editor):
    samples = apps.get_model("rest_api", "Sample")
    alignments = apps.get_model("rest_api", "Alignment")
    sequences = apps.get_model("rest_api", "Sequence")
    for sample in samples.objects.all():
        sequence = sequences.objects.get(seqhash=sample.seqhash)
        sample.sequence = sequence
        sample.save()
    for alignment in alignments.objects.all():
        sequence = sequences.objects.get(seqhash=alignment.seqhash)
        alignment.sequence = sequence
        alignment.save()


class Migration(migrations.Migration):
    dependencies = [
        ("rest_api", "0001_initial"),
    ]
    operations = [
        # remove foreign keys "seqhash" to sequence
        migrations.AlterField(
            model_name="alignment",
            name="seqhash",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="sample",
            name="seqhash",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        # add id to sequence
        migrations.AlterField(
            model_name="sequence",
            name="seqhash",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name="sequence",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        # add foreign keys "sequence" to sequence
        migrations.AddField(
            model_name="alignment",
            name="sequence",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="rest_api.sequence",
            ),
        ),
        migrations.AddField(
            model_name="sample",
            name="sequence",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="rest_api.sequence",
            ),
        ),
        # add foreign keys "sequence" to alignment, sample
        migrations.RunPython(insert_seqhash_ids),
        migrations.AlterField(
            model_name="lineages",
            name="lineage",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="elempart",
            name="element",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING, to="rest_api.element"
            ),
        ),
        migrations.AddField(
            model_name="elempart",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="lineages",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
