from django.contrib import admin
from .models import TimeSlot, Appointment


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('doctor', 'date')
    search_fields = ('doctor__username',)
    list_editable = ('is_booked',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'slot', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient__username',)
