# Generated by Django 4.2.7 on 2023-12-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_remove_invoice_num_aggregation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="date_aggregation",
            field=models.DateTimeField(null=True),
        ),
    ]
