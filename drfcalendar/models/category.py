from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.category_name