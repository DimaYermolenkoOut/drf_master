from django.contrib import admin

from drfcalendar.models import Service, MasterSchedule, Booking

# Rename Django Administration
admin.site.site_header = 'Hillel Django Administration'
admin.site.site_title = 'Hillel Django Administration'
admin.site.index_title = 'Welcome to Hillel Django Administration'


# Register your models here.
admin.site.register(Service)
admin.site.register(MasterSchedule)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('master_username', 'client_username', 'start_time', 'end_time', 'service_name')
    list_filter = ('master', 'client')
    list_editable = ('start_time', 'end_time')
    ordering = ('start_time', 'end_time', 'service')

    def master_username(self, obj):
        return obj.master.username

    def client_username(self, obj):
        return obj.client.username

    def service_name(self, obj):
        return obj.service.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('master', 'client', 'service')