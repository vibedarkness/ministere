# Generated by Django 4.2.5 on 2023-09-16 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_client_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="staff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.staff"
            ),
        ),
    ]
