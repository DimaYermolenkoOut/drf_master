import os
import django
from celery import shared_task

from authentication.models import User
from drfcalendar.availability import get_slots_for_service
from drfcalendar.models import Booking, Service
from datetime import datetime

from drfcalendar.serializers import SlotSerializer
from google_sheets.api import write_to_sheet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfmaster.settings')
django.setup()


@shared_task
def write_google_sheet_books_report_task():
    books = Booking.objects.all()
    print(books)

    # write to google sheet
    books_data = []
    for book in books:
        books_data.append([
            str(book.master),  # Convert to string
            str(book.service),  # Convert to string
            # str(book.date),  # Convert to string
            str(book.start_time),  # Convert to string
            str(book.end_time)  # Convert to string
        ])

        # Calculate the range based on data length
        range_end = 'E' + str(len(books_data) + 1)
        write_to_sheet(f"A1:{range_end}", books_data)

    # if __name__ == "__main__":
    #     write_google_sheet_books_report()


@shared_task
def hello_world_task():
    print('Hello, World!')


@shared_task()
def process_slots(master_id, service_id, date):
    master = User.objects.get(id=master_id)
    service = Service.objects.get(id=service_id)

    date_ = datetime.strptime(date, '%Y-%m-%d').date()

    slots = get_slots_for_service(master, date_, service)

    serialized_slots = SlotSerializer(slots, many=True).data
    return serialized_slots
    # print(serialized_slots)





# if __name__ == "__main__":
#     write_google_sheet_books_report()
# має такий вивід
# tube.ermolenko@gmail.com	less-2 90	2024-05-12 12:00:00+00:00	2024-05-12 13:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-12 14:00:00+00:00	2024-05-12 15:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-13 15:00:00+00:00	2024-05-13 16:30:00+00:00
# tube.ermolenko@gmail.com	less-1 60	2024-05-13 14:00:00+00:00	2024-05-13 15:00:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-14 13:00:00+00:00	2024-05-14 14:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-14 15:00:00+00:00	2024-05-14 16:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-14 10:00:00+00:00	2024-05-14 11:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-15 12:00:00+00:00	2024-05-15 13:30:00+00:00
# tube.ermolenko@gmail.com	less-2 90	2024-05-15 14:00:00+00:00	2024-05-15 15:30:00+00:00
# tube.ermolenko@gmail.com	less-1 60	2024-05-15 15:30:00+00:00	2024-05-15 16:30:00+00:00
# tube.ermolenko@gmail.com	less-1 60	2024-05-15 16:30:00+00:00	2024-05-15 17:30:00+00:00
# tube.ermolenko@gmail.com	less-1 60	2024-05-15 06:30:00+00:00	2024-05-15 07:30:00+00:00
# tube.ermolenko@gmail.com	less-1 60	2024-05-15 07:30:00+00:00	2024-05-15 08:30:00+00:00
