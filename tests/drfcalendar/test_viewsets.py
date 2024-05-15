from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from drfcalendar.models import Booking, Service, MasterSchedule  # Импорт модели MasterSchedule
from datetime import timedelta, datetime, time
from django.utils import timezone

class BookingViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.client.login(username='testuser', password='password')

        # Создание объекта MasterSchedule
        master_schedule = MasterSchedule.objects.create(
            master=self.user,
            working_days=[1, 2, 3, 4, 5],  # Пример рабочих дней (пн-пт)
            start_time=time(9, 0),  # Пример начального времени работы
            end_time=time(17, 0),   # Пример конечного времени работы
        )

        self.service = Service.objects.create(name='Test Service', duration=timedelta(minutes=60))

    def test_create_booking(self):
        url = 'http://127.0.0.1:8000/api/bookings/'
        data = {
            'master': self.user.id,
            'start_time': '2024-05-21T09:00:00Z',  # Assuming UTC time
            'end_time': '2024-05-21T10:00:00Z',
            'client': self.user.id,
            'service': 1,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().master, self.user)

    def test_delete_booking(self):
        booking = Booking.objects.create(
            master=self.user,
            start_time=timezone.make_aware(datetime(2024, 5, 15, 9, 0)),
            end_time=timezone.make_aware(datetime(2024, 5, 15, 10, 0)),
            client=self.user,
            service=self.service
        )
        url = reverse('booking-detail', args=[booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
