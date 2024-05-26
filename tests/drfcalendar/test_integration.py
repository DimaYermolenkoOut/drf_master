from datetime import datetime, time, timedelta
from django.utils import timezone

from django.test import TestCase

from authentication.models import User
from drfcalendar.models import Booking, MasterSchedule, Service

class IntegrationTestCase(TestCase):
    def test_bookings_api(self):
        # Создание объекта пользователя с обязательным полем email
        user = User.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )

        # Создание расписания для мастера
        MasterSchedule.objects.create(
            master=user,
            working_days=[0, 1, 2, 3, 4],  # Понедельник - Пятница
            start_time=time(8, 0),  # Начало рабочего дня в 08:00
            end_time=time(18, 0)  # Конец рабочего дня в 18:00
        )

        # Создание объекта сервиса
        service = Service.objects.create(
            name='testservice',
            duration=timedelta(hours=1)  # Длительность услуги 1 час
        )

        # Создание объекта бронирования
        Booking.objects.create(
            master=user,
            start_time=timezone.make_aware(datetime(2024, 5, 15, 9, 0)),
            end_time=timezone.make_aware(datetime(2024, 5, 15, 10, 0)),
            client=user,
            service=service
        )

        # Выполнение GET запроса к эндпоинту бронирования
        response = self.client.get('/bookings/')

        # Проверка, что статус-код ответа 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Проверка содержимого ответа
        self.assertEqual(response.json()['results'][0], {
            'master': 'testuser',
            'start_time': '2024-05-15T09:00:00Z',
            'end_time': '2024-05-15T10:00:00Z',
            'client': 'testuser',
            'service': 'testservice'
        })
