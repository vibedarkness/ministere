# Generated by Django 4.2.5 on 2023-09-16 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="staff",
            field=models.ForeignKey(
                default=2,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.staff",
            ),
        ),
    ]
