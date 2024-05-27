from django.db.migrations import serializer
from rest_framework import serializers

from authentication.models import User
from drfcalendar.models import Booking, Service, MasterSchedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'duration')


class BookingSerializer(serializers.ModelSerializer):
    master = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ('id', 'start_time', 'end_time', 'client', 'master', 'service')
        # fields = '__all__'





class MasterScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSchedule
        fields = ('id', 'master', 'working_days', 'start_time', 'end_time')