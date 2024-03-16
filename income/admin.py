from django.contrib import admin

# Register your models here.

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'amount', 'owner', 'date', 'description']

