from django.urls import path
from .views import (
    PatientRegistrationView,
    PatientLoginView,
    TokenRefreshView,
    PatientProfileView,
    PatientBookAppointmentView,
    PatientAppointmentsView,
    PatientCancelAppointmentView
)

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='patient-register'),
    path('login/', PatientLoginView.as_view(), name='patient-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='patient-token-refresh'),
    path('profile/<str:uid>/', PatientProfileView.as_view(), name='patient-profile'),
    path('book-appointment/<str:doctor_uid>/', PatientBookAppointmentView.as_view(), name='patient-book-appointment'),
    path('appointments/<str:patient_uid>/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('cancel-appointment/<str:booking_id>/', PatientCancelAppointmentView.as_view(), name='patient-cancel-appointment'),
]
