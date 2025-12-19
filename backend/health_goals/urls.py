from django.urls import path
from .views import (
    PatientHealthGoalView,
    PatientMedicalTestView,
    PatientPreventiveCheckupView,
    DoctorViewPatientHealthView
)

urlpatterns = [
    path('track/<str:patient_uid>/', PatientHealthGoalView.as_view(), name='health-goal-track'),
    path('medical-test/<str:patient_uid>/', PatientMedicalTestView.as_view(), name='add-medical-test'),
    path('medical-tests/<str:patient_uid>/', PatientMedicalTestView.as_view(), name='list-medical-tests'),
    path('preventive-checkup/<str:patient_uid>/', PatientPreventiveCheckupView.as_view(), name='add-preventive-checkup'),
    path('preventive-checkups/<str:patient_uid>/', PatientPreventiveCheckupView.as_view(), name='list-preventive-checkups'),
    path('doctor-view/<str:patient_uid>/', DoctorViewPatientHealthView.as_view(), name='doctor-view-patient-health'),
]
