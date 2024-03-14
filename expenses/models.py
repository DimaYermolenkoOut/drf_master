from django.db import models


# Create your models here.
class Expense(models.Model):

    CATEGORIES = (
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('RENT', 'RENT'),
        ('OTHERS', 'OTHERS'),
    )
    category = models.CharField(max_length=255, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
