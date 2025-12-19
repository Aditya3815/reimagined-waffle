from django.urls import path
from .views import (
    DoctorRegistrationView,
    DoctorLoginView,
    TokenRefreshView,
    DoctorProfileView,
    ToggleDoctorStatusView,
    DoctorListView,
    DoctorAvailabilityView,
    CheckDoctorAvailabilityView,
    BookAppointmentView,
    CancelAppointmentView,
    ListAppointmentsView
)

urlpatterns = [
    # Authentication endpoints
    path('register/', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile endpoints
    path('profile/<str:uid>/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('toggle-status/<str:uid>/', ToggleDoctorStatusView.as_view(), name='toggle-doctor-status'),
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    
    # Availability endpoints
    path('availability/<str:uid>/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('check-availability/<str:uid>/', CheckDoctorAvailabilityView.as_view(), name='check-doctor-availability'),
    
    # Appointment endpoints
    path('book-appointment/<str:doctor_uid>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('cancel-appointment/<str:booking_id>/', CancelAppointmentView.as_view(), name='cancel-appointment'),
    path('appointments/<str:doctor_uid>/', ListAppointmentsView.as_view(), name='list-appointments'),
]
