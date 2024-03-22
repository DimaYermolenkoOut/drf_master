# import unittest
# from drfcalendar.models.day import Day
# from datetime import datetime
#
# class TestDay(unittest.TestCase):
#     def test_book_slot(self):
#         day = Day('2024-03-23')
#         self.assertTrue(day.book_slot('11:00', 'Jon', 'driving', 'Dima', 60))
#         self.assertEqual(day.slots['11:00'], {'client_name': 'Jon', 'service_name': 'driving', 'master_name': 'Dima', 'duration': 60})
#         # self.assertEqual(day.book_slot('11:30', 'Vlad', 'driving', 'Dima', 30), "Slot is not available")
#         # self.assertEqual(day.slots['11:30'], {'client_name': 'Vlad', 'service_name': 'driving', 'master_name': 'Dima', 'duration': 30})
#
#     def test_get_available_slots(self):
#         day = Day('2024-03-23')
#         self.assertEqual(day.get_available_slots(), {
#             '9:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '9:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '10:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '10:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '11:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '11:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '12:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '12:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '13:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '13:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '14:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '14:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '15:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '15:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '16:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '16:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '17:00': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#             '17:30': {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0},
#         })
#
#     def test_cancel_slot(self):
#         day = Day('2024-03-23')
#         day.book_slot('11:00', 'Jon', 'driving', 'Dima', 60)
#         self.assertTrue(day.cancel_slot('11:00'))
#         self.assertEqual(day.slots['11:00'], {'client_name': '', 'service_name': '', 'master_name': '', 'duration': 0})
#
#


import unittest
from datetime import datetime, timedelta

from drfcalendar.models import Day


class DayTest(unittest.TestCase):

    def setUp(self):
        self.day = Day('2024-03-25')  # Use a future date to avoid conflicts with real appointments

    def test_init(self):
        self.assertEqual(self.day.data, '2024-03-25')  # Verify date is correctly stored
        self.assertEqual(len(self.day.slots), 18)  # Ensure all time slots are initialized
        for time, info in self.day.slots.items():
            self.assertEqual(info, {
                "client_name": "",
                "service_name": "",
                "master_name": "",
                "duration": 0
            })  # Verify initial slot information

    def test_book_slot_success(self):
        # Successful booking
        success = self.day.book_slot('10:00', 'Alice', 'haircut', 'Bob', 30)  # Duration in minutes
        self.assertTrue(success)

        # Verify slot information is updated
        slot = self.day.slots['10:00']
        self.assertEqual(slot['client_name'], 'Alice')
        self.assertEqual(slot['service_name'], 'haircut')
        self.assertEqual(slot['master_name'], 'Bob')
        self.assertEqual(slot['duration'], 30)  # Duration should be in minutes

        # Verify subsequent slots are blocked for the duration
        for time in ['10:30', '10:45', '10:59']:
            self.assertEqual(self.day.slots[time], False)  # Blocked due to slot duration

    def test_book_slot_failure_existing_booking(self):
        # Booking in an already occupied slot
        self.day.book_slot('11:00', 'Bob', 'massage', 'Jane', 45)  # Duration in minutes
        success = self.day.book_slot('11:00', 'Charlie', 'waxing', 'Lisa', 60)
        self.assertFalse(success)

        # Verify original booking remains
        slot = self.day.slots['11:00']
        self.assertEqual(slot['client_name'], 'Bob')
        self.assertEqual(slot['service_name'], 'massage')
        self.assertEqual(slot['master_name'], 'Jane')
        self.assertEqual(slot['duration'], 45)  # Duration should be in minutes

    def test_book_slot_failure_invalid_time(self):
        # Booking outside available times
        success = self.day.book_slot('18:00', 'David', 'yoga', 'Emily', 90)  # Duration in minutes
        self.assertFalse(success)

        # Verify slots remain unchanged
        for time, info in self.day.slots.items():
            self.assertNotEqual(info, {
                "client_name": "David",
                "service_name": "yoga",
                "master_name": "Emily",
                "duration": 90
            })

    def test_get_available_slots(self):
        # Book a slot
        self.day.book_slot('12:00', 'Eve', 'facial', 'Max', 75)  # Duration in minutes

        available_slots = self.day.get_available_slots()

        self.assertEqual(available_slots, {
            '12:00': {
                'client_name': 'Eve',
                'service_name': 'facial',
                'master_name': 'Max',
                'duration': 75
            }
        })
