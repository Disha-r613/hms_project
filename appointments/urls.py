from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('success/', views.success, name='success'),
    path('my/', views.my_appointments, name='my_appointments'),
]
