from django.db.migrations import serializer
from rest_framework import serializers

from drfcalendar.models import Booking


class SlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'start_time', 'end_time', 'client', 'master', 'service')