# Generated by Django 4.0.6 on 2024-01-10 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_invoice_date_fin_alter_invoice_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_aggregation',
            field=models.DateTimeField(null=True),
        ),
    ]
