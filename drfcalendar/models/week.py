from django.db import models

from drfcalendar.models import Day


class Week(models.Model):

    days = models.ForeignKey(Day, on_delete=models.CASCADE)