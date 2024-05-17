from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError
from rest_framework import status

from authentication.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drfcalendar.availability import get_slots_for_service
from drfcalendar.models import Service, Booking
from drfcalendar.serializers import SlotSerializer, BookingSerializer, ServiceSerializer
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from collections import defaultdict

# виводить слоти за один день
@api_view(['GET'])
def slots(request, master_id, service_id, date):
    master = User.objects.get(id=master_id)
    service = Service.objects.get(id=service_id)

    date_ = datetime.strptime(date, '%Y-%m-%d').date()

    slots = get_slots_for_service(master, date_, service)

    return Response(SlotSerializer(slots, many=True).data)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date in the format YYYY-MM-DD", type=openapi.TYPE_STRING),
    openapi.Parameter('days_ahead', openapi.IN_QUERY, description="Number of days ahead to check availability", type=openapi.TYPE_INTEGER),
])
# слоти на декілька днів вперед
@api_view(['GET'])
def slots_view(request, master_id, service_id):
    start_date_str = request.GET.get('start_date')
    days_ahead = int(request.GET.get('days_ahead', 1))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date.today()
    end_date = start_date + timedelta(days=days_ahead)

    master = User.objects.get(id=master_id)
    service = Service.objects.get(id=service_id)

    slots_data = defaultdict(list)
    while start_date < end_date:
        slots = get_slots_for_service(master, start_date, service)
        slots_data[start_date.strftime('%Y-%m-%d')].extend(SlotSerializer(slots, many=True).data)
        start_date += timedelta(days=1)

    return JsonResponse(slots_data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer