from django.db import models


DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)


class Days(models.Model):
    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    class Meta:
        ordering = ('day',)
        verbose_name = 'День'
        verbose_name_plural = 'Дни'

    def __str__(self):
        return self.day


class StartTime(models.Model):
    time = models.TimeField(max_length=30)
    days = models.ManyToManyField(Days)
    # date = models.DateField(max_length=30)
