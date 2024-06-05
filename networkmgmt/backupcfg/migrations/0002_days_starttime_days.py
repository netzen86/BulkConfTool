# Generated by Django 4.1.4 on 2024-06-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backupcfg", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Days",
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
                ("day", models.CharField(max_length=8)),
            ],
        ),
        migrations.AddField(
            model_name="starttime",
            name="days",
            field=models.ManyToManyField(to="backupcfg.days"),
        ),
    ]
