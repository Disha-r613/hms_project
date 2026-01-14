from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import TimeSlot, Appointment


@login_required
def book_appointment(request):

    # ❌ block admin & doctors
    if request.user.is_staff or getattr(request.user, 'is_doctor', False):
        return HttpResponseForbidden("Only patients can book appointments.")

    slots = TimeSlot.objects.filter(is_booked=False)

    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        slot = TimeSlot.objects.get(id=slot_id)

        Appointment.objects.create(
            patient=request.user,
            slot=slot
        )

        slot.is_booked = True
        slot.save()

        return redirect('success')

    return render(request, 'appointments/book.html', {'slots': slots})


def success(request):
    return render(request, 'appointments/success.html')
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments
    })
