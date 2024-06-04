from django.db import models


class StartTime(models.Model):
    date = models.DateField(max_length=30)
    time = models.TimeField(max_length=30)
