from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from authentication.models import User
from drfcalendar.availability import get_slots_for_service
from telegram.client import send_message


class Service(models.Model):
    name = models.CharField(max_length=120)
    duration = models.DurationField()

    def __str__(self):
        return self.name


class MasterSchedule(models.Model):
    master = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_schedule')
    working_days = ArrayField(models.IntegerField())
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.master.email


class Booking(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def clean(self):
        slots = get_slots_for_service(self.master, self.start_time.date(), self.service)

        if not any(slot.start_time == self.start_time.time() and slot.end_time == self.end_time.time() for slot in slots):
            raise ValidationError('Booking does not fit into slot')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)


@receiver(models.signals.post_save, sender=Booking)
def send_booking_telegram_message(sender, instance, created, **kwargs):
    if created:
        chat_id = 6740309896

        send_message(chat_id, message=f'Ваша заявка прийнята на {instance.start_time}')


# send Email post_save Booking
# @receiver(models.signals.post_save, sender=Booking)
# def send_booking_email(sender, instance, created, **kwargs):
#     if created:
#