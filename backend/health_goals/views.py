from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from firebase_admin import firestore
from backend.firebase_init import db
from datetime import datetime
import uuid
from .serializers import (
    HealthGoalSerializer,
    MedicalTestSerializer,
    PreventiveCheckupSerializer,
    HealthGoalSummarySerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class PatientHealthGoalView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_uid):
        serializer = HealthGoalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        tracking_date = str(data['date'])
        
        try:
            doc_id = f"{patient_uid}_{tracking_date}"
            
            tracking_data = {
                'patient_uid': patient_uid,
                'date': tracking_date,
                'steps_taken': data.get('steps_taken', 0),
                'hours_sleep': data.get('hours_sleep', 0),
                'water_intake': data.get('water_intake', 0),
                'calories_consumed': data.get('calories_consumed', 0),
                'exercise_minutes': data.get('exercise_minutes', 0),
                'notes': data.get('notes', ''),
                'updated_at': firestore.SERVER_TIMESTAMP
            }
            
            db.collection('health_tracking').document(doc_id).set(tracking_data, merge=True)
            
            return Response({
                'message': 'Health goals tracked successfully',
                'data': tracking_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, patient_uid):
        tracking_date = request.query_params.get('date')
        
        try:
            if tracking_date:
                doc_id = f"{patient_uid}_{tracking_date}"
                doc = db.collection('health_tracking').document(doc_id).get()
                
                if doc.exists:
                    return Response(doc.to_dict(), status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No data for this date'}, status=status.HTTP_404_NOT_FOUND)
            else:
                docs = db.collection('health_tracking').where('patient_uid', '==', patient_uid).stream()
                
                tracking_list = []
                for doc in docs:
                    tracking_list.append(doc.to_dict())
                
                tracking_list.sort(key=lambda x: x.get('date', ''), reverse=True)
                
                return Response({
                    'count': len(tracking_list),
                    'tracking': tracking_list
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PatientMedicalTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_uid):
        serializer = MedicalTestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            test_id = str(uuid.uuid4())
            
            test_data = {
                'test_id': test_id,
                'patient_uid': patient_uid,
                'test_name': data['test_name'],
                'test_date': str(data['test_date']),
                'test_result': data.get('test_result', ''),
                'doctor_name': data.get('doctor_name', ''),
                'notes': data.get('notes', ''),
                'file_url': data.get('file_url', ''),
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            db.collection('medical_tests').document(test_id).set(test_data)
            
            return Response({
                'message': 'Medical test added successfully',
                'test_id': test_id,
                'data': test_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, patient_uid):
        try:
            docs = db.collection('medical_tests').where('patient_uid', '==', patient_uid).stream()
            
            tests = []
            for doc in docs:
                tests.append(doc.to_dict())
            
            tests.sort(key=lambda x: x.get('test_date', ''), reverse=True)
            
            return Response({
                'count': len(tests),
                'tests': tests
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PatientPreventiveCheckupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_uid):
        serializer = PreventiveCheckupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            checkup_id = str(uuid.uuid4())
            
            checkup_data = {
                'checkup_id': checkup_id,
                'patient_uid': patient_uid,
                'checkup_type': data['checkup_type'],
                'checkup_date': str(data['checkup_date']),
                'doctor_name': data.get('doctor_name', ''),
                'findings': data.get('findings', ''),
                'next_checkup_date': str(data.get('next_checkup_date', '')),
                'notes': data.get('notes', ''),
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            db.collection('preventive_checkups').document(checkup_id).set(checkup_data)
            
            return Response({
                'message': 'Preventive checkup added successfully',
                'checkup_id': checkup_id,
                'data': checkup_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, patient_uid):
        try:
            docs = db.collection('preventive_checkups').where('patient_uid', '==', patient_uid).stream()
            
            checkups = []
            for doc in docs:
                checkups.append(doc.to_dict())
            
            checkups.sort(key=lambda x: x.get('checkup_date', ''), reverse=True)
            
            return Response({
                'count': len(checkups),
                'checkups': checkups
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorViewPatientHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patient_uid):
        try:
            patient_ref = db.collection('patients').document(patient_uid)
            patient_doc = patient_ref.get()
            
            if not patient_doc.exists:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
            
            patient_data = patient_doc.to_dict()
            patient_data.pop('password', None)
            
            tracking_docs = db.collection('health_tracking').where('patient_uid', '==', patient_uid).stream()
            tracking_list = [doc.to_dict() for doc in tracking_docs]
            tracking_list.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            test_docs = db.collection('medical_tests').where('patient_uid', '==', patient_uid).stream()
            tests = [doc.to_dict() for doc in test_docs]
            tests.sort(key=lambda x: x.get('test_date', ''), reverse=True)
            
            checkup_docs = db.collection('preventive_checkups').where('patient_uid', '==', patient_uid).stream()
            checkups = [doc.to_dict() for doc in checkup_docs]
            checkups.sort(key=lambda x: x.get('checkup_date', ''), reverse=True)
            
            total_days = len(tracking_list)
            avg_steps = sum(t.get('steps_taken', 0) for t in tracking_list) / total_days if total_days > 0 else 0
            avg_sleep = sum(t.get('hours_sleep', 0) for t in tracking_list) / total_days if total_days > 0 else 0
            
            return Response({
                'patient_info': {
                    'uid': patient_data.get('uid'),
                    'name': f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}",
                    'email': patient_data.get('email'),
                    'phone_number': patient_data.get('phone_number'),
                    'date_of_birth': patient_data.get('date_of_birth'),
                    'address': patient_data.get('address'),
                    'emergency_contact': patient_data.get('emergency_contact')
                },
                'health_summary': {
                    'total_days_tracked': total_days,
                    'avg_steps_per_day': round(avg_steps, 2),
                    'avg_sleep_hours': round(avg_sleep, 2),
                    'total_medical_tests': len(tests),
                    'total_preventive_checkups': len(checkups)
                },
                'recent_tracking': tracking_list[:30],
                'medical_tests': tests,
                'preventive_checkups': checkups
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
