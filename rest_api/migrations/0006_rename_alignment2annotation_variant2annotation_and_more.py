# Generated by Django 4.1.6 on 2023-08-10 08:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rest_api", "0005_alignment_variants_alter_element_sequence_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Alignment2Annotation",
            new_name="Variant2Annotation",
        ),
        migrations.AlterModelTable(
            name="variant2annotation",
            table="variant2annotation",
        ),
    ]
