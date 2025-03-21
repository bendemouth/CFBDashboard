# Generated by Django 5.1.7 on 2025-03-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CFBDash", "0003_team_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
