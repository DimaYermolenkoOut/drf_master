from dataclasses import dataclass
from datetime import date, time, datetime, timedelta

from django.contrib.auth.models import User


@dataclass
class Slot:
    start_time: time
    end_time: time


def get_availability(master: User, date_: date):
    schedule = master.master_schedule

    if date_.weekday() not in schedule.working_days:
        return []

    # Master is busy on these times
    bookings = master.master_bookings.filter(start_time__date=date_).order_by('start_time')
    # bookings = Booking.objects.filter(master=master, start_time__date=date_)

    # Master is available on these times
    availability = []

    start_time = schedule.start_time

    for booking in bookings:
        availability.append(Slot(start_time, booking.start_time.time()))
        start_time = booking.end_time.time()

    availability.append(Slot(start_time, schedule.end_time))

    # Filter out availability that is 0 minutes
    availability = [a for a in availability if a.start_time != a.end_time]

    return availability


def get_slots_for_service(master, date_, service):
    # 09:00 - 13:00 , 14:00 - 18:00, 18:30 - 19:00
    availability_slots = get_availability(master, date_)

    # Divide slots into smaller slots based on the service duration
    # 09:00 - 10:00, 10:00 - 11:00, 11:00 - 12:00, 12:00 - 13:00 ...
    service_slots = []
    for slot in availability_slots:
        # 10:00
        start_time = datetime.combine(date_, slot.start_time)
        while start_time < datetime.combine(date_, slot.end_time):
            # 11:00
            end_time = (start_time + service.duration)

            if end_time > datetime.combine(date_, slot.end_time):
                break

            service_slots.append(Slot(start_time.time(), end_time.time()))
            # start_time = end_time
            start_time += timedelta(minutes=30)

    return service_slots

# get slots for service ahead for {} days
# def get_slots_for_service_ahead(master, date_, service, days):
#     # 09:00 - 13:00 , 14:00 - 18:00, 18:30 - 19:00
#     availability_slots = get_availability(master, date_)
#
#     # Divide slots into smaller slots based on the service duration
#     # 09:00 - 10:00, 10:00 - 11:00, 11:00 - 12:00, 12:00 - 13:00 ...
#     service_slots = []
#     for slot in availability_slots:
#         # 10:00
#         start_time = datetime.combine(date_, slot.start_time)
#         while start_time < datetime.combine(date_, slot.end_time):
#             # 11:00
#             end_time = (start_time + service.duration)
#
#             if end_time > datetime.combine(date_, slot.end_time):
#                 break
#
#             service_slots.append(Slot(start_time.time(), end_time.time()))
#             # start_time = end_time
#             start_time += timedelta(days=days, minutes=30)
#
#     return service_slots