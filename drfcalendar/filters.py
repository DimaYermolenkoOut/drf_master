import django_filters

from drfcalendar.models import Booking


class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'master': ['exact'],
            'start_time': ['exact', 'gte', 'lte'],
            'end_time': ['exact', 'gte', 'lte'],
            'client': ['exact'],
            'service': ['exact'],
        }


class SlotFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'start_time': ['exact', 'gte', 'lte'],
            'end_time': ['exact', 'gte', 'lte'],
            'service': ['exact'],
            'master': ['exact'],
            'client': ['exact'],
        }