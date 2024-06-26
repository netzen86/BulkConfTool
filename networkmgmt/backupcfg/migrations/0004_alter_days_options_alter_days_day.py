# Generated by Django 4.1.4 on 2024-06-05 17:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backupcfg", "0003_remove_starttime_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="days",
            options={
                "ordering": ("day",),
                "verbose_name": "День",
                "verbose_name_plural": "Дни",
            },
        ),
        migrations.AlterField(
            model_name="days",
            name="day",
            field=models.CharField(
                choices=[
                    (0, "Monday"),
                    (1, "Tuesday"),
                    (2, "Wednesday"),
                    (3, "Thursday"),
                    (4, "Friday"),
                    (5, "Saturday"),
                    (6, "Sunday"),
                ],
                max_length=1,
            ),
        ),
    ]
