from rest_framework import serializers

from income.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date', 'description', 'owner']