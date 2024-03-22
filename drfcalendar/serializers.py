

def AppointmentSerializer:

    class Meta:
        model = Appointment
        fields = ['start_time', 'duration', 'available_times']
