# Generated by Django 4.2 on 2024-02-18 08:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("default", "0002_profile_profile_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("patient", models.CharField(max_length=100, null=True)),
            ],
        ),
    ]