from django.contrib import admin

from authentication import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username']