# Generated by Django 4.2 on 2024-02-18 08:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("default", "0005_appointment"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Appointment",
        ),
    ]