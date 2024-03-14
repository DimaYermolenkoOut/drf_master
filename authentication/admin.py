from django.contrib import admin

from authentication import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username']