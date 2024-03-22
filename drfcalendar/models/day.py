from django.db import models
from datetime import datetime, timedelta

from authentication.models import User
from drfcalendar.models import Service


class Slot(models.Model):
    time = models.TimeField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_slots', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_slots', blank=True, null=True)
    duration = models.IntegerField(default=0)
    is_booked = models.BooleanField(default=False)


class Day(models.Model):
    data = models.DateField()
    slots = models.ManyToManyField(Slot)
    week = models.ForeignKey('Week', on_delete=models.CASCADE, related_name='week_days')

    def book_slot(self, time, client_name, service_name, master_name, duration):
        slot = self.slots.get(time=time)
        if slot.client_name == "":
            slot.client_name = client_name
            slot.service_name = service_name
            slot.master_name = master_name
            slot.duration = duration
            slot.save()

            # Преобразование строки времени в объект datetime
            time_obj = datetime.strptime(str(time), '%H:%M')
            # Прибавление длительности услуги
            end_time_obj = time_obj + timedelta(minutes=duration)
            # Преобразование обратно в строку
            end_time_str = end_time_obj.strftime('%H:%M')
            # Обновление всех слотов, которые входят в длительность услуги
            for slot in self.slots.all():
                if str(time) < str(slot.time) < end_time_str:
                    self.slots.remove(slot)
            return True
        return False

    def get_available_slots(self):
        return self.slots.filter(service_name="")

    # отменить слот записи
    def cancel_slot(self, time):
        slot = self.slots.get(time=time)
        slot.client_name = ""
        slot.service_name = ""
        slot.master_name = ""
        slot.duration = 0
        slot.save()
        return True
