import unittest
from drfcalendar.models.day import Day
from datetime import datetime

class TestDay(unittest.TestCase):
    def setUp(self):
        self.day = Day('2024-03-23')

    def test_slots_initialization(self):
        self.assertEqual(self.day.data, '2024-03-23')
        self.assertIn('9:00', self.day.slots)
        self.assertIn('17:30', self.day.slots)
        self.assertEqual(self.day.slots['9:00']['duration'], 0)

    def test_book_slot(self):
        # Проверка бронирования слота
        result = self.day.book_slot('9:00', 'client1', 'service1', 'master1', 60)
        self.assertTrue(result)
        self.assertEqual(self.day.slots['9:00']['client_name'], 'client1')

        # Проверка попытки бронирования уже занятого слота
        result = self.day.book_slot('9:00', 'client2', 'service2', 'master2', 30)
        self.assertFalse(result)
        self.assertEqual(self.day.slots['9:00']['client_name'], 'client1')  # имя клиента не изменилось


    def test_get_available_slots(self):
        # Проверка наличия доступных слотов
        result = self.day.get_available_slots()
        self.assertIn('9:00', result)
        self.assertIn('10:00', result)
        self.assertIn('11:00', result)
        self.assertIn('12:00', result)
        self.assertIn('13:00', result)
        self.assertIn('14:00', result)
        self.assertIn('15:00', result)
        self.assertIn('16:00', result)
        self.assertIn('17:00', result)

if __name__ == '__main__':
    unittest.main()
