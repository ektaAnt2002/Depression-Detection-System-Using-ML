# Generated by Django 4.2 on 2024-02-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_remove_appointments_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointments",
            name="description",
            field=models.TextField(null=True),
        ),
    ]