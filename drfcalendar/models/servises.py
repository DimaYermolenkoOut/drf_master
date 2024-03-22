from django.db import models

from authentication.models import User
from drfcalendar.models.category import Category


class Service(models.Model):
    service_name = models.CharField(max_length=255, unique=True, null=True)
    discription = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_services', blank=True, null=True)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_services', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    expenses = models.ManyToManyField(User, related_name='expenses', blank=True)

    available = models.BooleanField(default=True)





    def __str__(self):
        return self.service_name