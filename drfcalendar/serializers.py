from django.db.migrations import serializer
from rest_framework import serializers

from drfcalendar.models import Booking, Service, MasterSchedule


class SlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        # fields = ('id', 'start_time', 'end_time', 'client', 'master', 'service')
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'duration')


class MasterScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSchedule
        fields = ('id', 'master', 'working_days', 'start_time', 'end_time')