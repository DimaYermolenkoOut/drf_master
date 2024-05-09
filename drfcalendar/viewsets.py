from datetime import datetime

from authentication.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drfcalendar.availability import get_slots_for_service
from drfcalendar.models import Service, Booking
from drfcalendar.serializers import SlotSerializer, BookingSerializer


@api_view(['GET'])
def slots(request, master_id, service_id, date):
    master = User.objects.get(id=master_id)
    service = Service.objects.get(id=service_id)

    date_ = datetime.strptime(date, '%Y-%m-%d').date()

    slots = get_slots_for_service(master, date_, service)

    return Response(SlotSerializer(slots, many=True).data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# @api_view(['POST'])
# def book(request, master_id, service_id, date, start_time, end_time):
#     master = User.objects.get(id=master_id)
#     service = Service.objects.get(id=service_id)
#
#     date_ = datetime.strptime(date, '%Y-%m-%d').date()
#     start_time = datetime.strptime(start_time, '%H:%M').time()
#     end_time = datetime.strptime(end_time, '%H:%M').time()
#
#     booking = Booking.objects.create(
#         start_time=datetime.combine(date_, start_time),
#         end_time=datetime.combine(date_, end_time),
#         client=request.user,
#         master=master,
#         service=service
#     )

    # return Response(BookingSerializer(booking).data)
