from django.test import TestCase
from django.core.exceptions import ValidationError
from drfcalendar.models import Service, MasterSchedule, Booking
from datetime import timedelta, datetime, time
from django.utils import timezone
import pytz
from drfcalendar.availability import get_slots_for_service, Slot  # Импортируем get_slots_for_service и Slot

# Імпортуємо призначену для користувача модель User із додатка authentication
from authentication.models import User

class ServiceModelTest(TestCase):
    def test_service_creation(self):
        service = Service.objects.create(name='Haircut', duration=timedelta(minutes=30))
        self.assertEqual(service.name, 'Haircut')
        self.assertEqual(service.duration, timedelta(minutes=30))

class MasterScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_master_schedule_creation(self):
        schedule = MasterSchedule.objects.create(
            master=self.user,
            working_days=[0, 1, 2, 3, 4],
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        self.assertEqual(schedule.master, self.user)
        self.assertEqual(schedule.working_days, [0, 1, 2, 3, 4])
        self.assertEqual(schedule.start_time, time(9, 0))
        self.assertEqual(schedule.end_time, time(17, 0))

class BookingModelTest(TestCase):
    def setUp(self):
        self.master = User.objects.create_user(username='master', email='master@example.com', password='password')
        self.client = User.objects.create_user(username='client', email='client@example.com', password='password')
        self.service = Service.objects.create(name='Massage', duration=timedelta(hours=1))

        self.schedule = MasterSchedule.objects.create(
            master=self.master,
            working_days=[0, 1, 2, 3, 4],
            start_time=time(9, 0),
            end_time=time(17, 0)
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            master=self.master,
            start_time=timezone.make_aware(datetime(2024, 5, 15, 9, 0)),
            end_time=timezone.make_aware(datetime(2024, 5, 15, 10, 0)),
            client=self.client,
            service=self.service
        )
        self.assertEqual(booking.master, self.master)
        self.assertEqual(booking.start_time, timezone.make_aware(datetime(2024, 5, 15, 9, 0)))
        self.assertEqual(booking.end_time, timezone.make_aware(datetime(2024, 5, 15, 10, 0)))
        self.assertEqual(booking.client, self.client)
        self.assertEqual(booking.service, self.service)

    def test_booking_clean_method(self):
        # Mocking get_slots_for_service function
        def mock_get_slots_for_service(master, date, service):
            return [
                Slot(start_time=time(9, 0), end_time=time(10, 0)),
                Slot(start_time=time(10, 0), end_time=time(11, 0))
            ]

        # Replace the original function with the mock
        import drfcalendar.availability
        drfcalendar.availability.get_slots_for_service = mock_get_slots_for_service

        booking = Booking(
            master=self.master,
            start_time=timezone.make_aware(datetime(2024, 5, 15, 9, 0)),
            end_time=timezone.make_aware(datetime(2024, 5, 15, 10, 0)),
            client=self.client,
            service=self.service
        )

        try:
            booking.full_clean()  # This should not raise a ValidationError
        except ValidationError:
            self.fail('Booking clean method raised ValidationError unexpectedly!')

        # Test invalid slot
        invalid_booking = Booking(
            master=self.master,
            start_time=timezone.make_aware(datetime(2024, 5, 15, 8, 0)),
            end_time=timezone.make_aware(datetime(2024, 5, 15, 9, 0)),
            client=self.client,
            service=self.service
        )

        with self.assertRaises(ValidationError):
            invalid_booking.full_clean()
