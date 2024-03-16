from django.db import models


# Create your models here.
class Income(models.Model):

    SOURCE = (
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('PRESENT', 'PRESENT'),
        ('OTHERS', 'OTHERS'),
    )
    source = models.CharField(max_length=255, choices=SOURCE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner) + "'s income"
