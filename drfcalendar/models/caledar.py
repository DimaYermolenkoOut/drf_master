from datetime import datetime


class Calendar:
    def __init__(self):
        self.slots = {}

    def add_day(self, day):
        self.slots[day] = {
            "9:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "9:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "10:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "10:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "11:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "11:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "12:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "12:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "13:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "13:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "14:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "14:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "15:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "15:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "16:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "16:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},
            "17:00": {"client_name": "", "service_name": "", "master_name": "", "duration": 0},

            "17:30": {"client_name": "", "service_name": "", "master_name": "", "duration": 0}
        }

    def book_slot(self, day, time, client_name, service_name, master_name, duration):
        now = datetime.now()
        booking_date = datetime.strptime(day, "%Y-%m-%d")
        if booking_date.date() >= now.date():
            if day in self.slots and time in self.slots[day] and self.slots[day][time][
                "client_name"] == "":
                slot_duration = self.slots[day][time]["duration"]
                if slot_duration >= duration:
                    self.slots[day][time] = {
                        "client_name": client_name,
                        "service_name": service_name,
                        "master_name": master_name,
                        "duration": duration
                    }
                    return True
        return False

    def get_available_slots(self, day, service_duration, start_time):
        now = datetime.now()
        booking_date = datetime.strptime(day, "%Y-%m-%d")
        if booking_date.date() >= now.date():
            if day in self.slots:
                available_slots = []
                for time, info in self.slots[day].items():
                    if info["client_name"] == "" and time >= start_time:
                        # slot_duration = self.slots[day][time]["duration"]
                        # slot_duration = info["duration"]
                        # if slot_duration >= service_duration:
                            available_slots.append(time)
                return available_slots
        return []


# Создание календаря
calendar = Calendar()
# Добавление дня в календарь
calendar.add_day("2024-03-23")
print(calendar.slots)

# Запись слота в календарь
calendar.book_slot("2024-03-23", "10:00", "John", "Service 1", "Master 1", 60)
print(calendar.slots)

start_time = "10:00"
service_duration = 60
available_slots = calendar.get_available_slots("2024-03-23", service_duration, start_time)
print(available_slots)