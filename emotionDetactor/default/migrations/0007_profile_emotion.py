# Generated by Django 4.2 on 2024-02-18 10:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("default", "0006_delete_appointment"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="emotion",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
