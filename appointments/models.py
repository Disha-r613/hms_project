from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TimeSlot(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_doctor': True}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor} | {self.date} | {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_patient': True}
    )
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # auto fill date from slot
        self.date = self.slot.date
        self.slot.is_booked = True
        self.slot.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} → {self.slot}"
