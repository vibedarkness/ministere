# Generated by Django 4.2.5 on 2024-01-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_client_couleur_statut"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="date_fin",
        ),
        migrations.AlterField(
            model_name="invoice",
            name="date_creation",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]