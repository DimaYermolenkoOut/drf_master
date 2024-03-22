from datetime import datetime, timedelta

class Day:
    def __init__(self, data):
        self.data = data
        self.slots = {
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

    def book_slot(self, time, client_name, service_name, master_name, duration):
        slot = self.slots.get(time)
        if slot["client_name"] == "":

            slot.update({
                "client_name": client_name,
                "service_name": service_name,
                "master_name": master_name,
                "duration": duration
            })
            # Преобразование строки времени в объект datetime
            time_obj = datetime.strptime(time, '%H:%M')
            # Прибавление длительности услуги
            end_time_obj = time_obj + timedelta(minutes=duration)
            # Преобразование обратно в строку
            end_time_str = end_time_obj.strftime('%H:%M')
            # Обновление всех слотов, которые входят в длительность услуги
            for slot_time in self.slots:
                if time < slot_time < end_time_str:
                    self.slots[slot_time] = False
            return True
        return False

    def get_available_slots(self):
        available_slots = {}
        for time, info in self.slots.items():
            if info["service_name"] == "":
                available_slots[time] = info
        return available_slots



# пример создания записи в календарь
day = Day('2024-03-23')
day.book_slot('11:00', 'Jon', 'driving', 'Dima', 60)
# day.book_slot('11:30', 'Vlad', 'driving', 'Dima', 30)

# пример получения доступных слотов
for time, info in day.slots.items():
    if info == False or info["service_name"] != "":
        continue
    else:
        print(time)
booked_slots = dict()
# пример получения занятых слотов
for time, info in day.slots.items():
    if info != False and info["service_name"] != "":
        booked_slots[time] = info

print(booked_slots)




