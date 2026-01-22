from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from urllib.parse import urlencode

from .models import TimeSlot, Appointment


@login_required
def book_appointment(request):

    # block admin / doctors
    if request.user.is_staff or getattr(request.user, 'is_doctor', False):
        return HttpResponseForbidden("Only patients can book appointments.")

    slots = TimeSlot.objects.filter(is_booked=False)

    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        slot = TimeSlot.objects.get(id=slot_id)

        appointment = Appointment.objects.create(
            patient=request.user,
            slot=slot
        )

        slot.is_booked = True
        slot.save()

        # -------- GOOGLE CALENDAR LINK (NO API) --------
        start = slot.start_time.strftime("%Y%m%dT%H%M%S")
        end = slot.end_time.strftime("%Y%m%dT%H%M%S")

        params = urlencode({
            "action": "TEMPLATE",
            "text": "Doctor Appointment",
            "dates": f"{start}/{end}",
            "details": "Hospital appointment booking",
        })

        calendar_link = f"https://calendar.google.com/calendar/render?{params}"

        # -------- EMAIL (LOCAL / CONSOLE) --------
        send_mail(
            subject="Appointment Confirmed",
            message=f"""
Your appointment is confirmed.

Date & Time: {slot.start_time}

Add to Google Calendar:
{calendar_link}
""",
            from_email="noreply@hms.com",
            recipient_list=[request.user.email],
            fail_silently=True,
        )

        # store link in session to show on success page
        request.session['calendar_link'] = calendar_link

        return redirect('success')

    return render(request, 'appointments/book.html', {'slots': slots})


@login_required
def success(request):
    calendar_link = request.session.get('calendar_link')
    return render(request, 'appointments/success.html', {
        'calendar_link': calendar_link
    })


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments
    })

