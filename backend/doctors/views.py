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
    DoctorRegistrationSerializer,
    DoctorLoginSerializer,
    DoctorProfileSerializer,
    AvailabilitySerializer,
    BookAppointmentSerializer
)
from .auth import hash_password, verify_password, generate_jwt_token, JWTAuthentication


@method_decorator(csrf_exempt, name='dispatch')
class DoctorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        email = data['email']
        password = data.pop('password')
        data.pop('password_confirm')

        try:
            doctors_ref = db.collection('doctors')
            existing = doctors_ref.where('email', '==', email).limit(1).stream()
            if any(existing):
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            uid = str(uuid.uuid4())
            hashed_password = hash_password(password)

            doctor_data = {
                'uid': uid,
                'email': email,
                'password': hashed_password,
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone_number': data.get('phone_number', ''),
                'specialization': data.get('specialization', ''),
                'license_number': data.get('license_number', ''),
                'years_of_experience': data.get('years_of_experience', 0),
                'bio': data.get('bio', ''),
                'profile_picture': '',
                'is_verified': False,
                'is_active': True,
                'availability': [],
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }

            db.collection('doctors').document(uid).set(doctor_data)
            tokens = generate_jwt_token(uid, email)

            response_data = {
                'uid': uid,
                'email': email,
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone_number': data.get('phone_number', ''),
                'specialization': data.get('specialization', ''),
                'license_number': data.get('license_number', ''),
                'years_of_experience': data.get('years_of_experience', 0),
                'bio': data.get('bio', ''),
                'profile_picture': '',
                'is_verified': False,
                'is_active': True,
                'availability': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            return Response({
                'message': 'Doctor registered successfully',
                'doctor': response_data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_201)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            doctors_ref = db.collection('doctors')
            docs = doctors_ref.where('email', '==', email).limit(1).stream()
            
            doctor_doc = None
            for doc in docs:
                doctor_doc = doc
                break
            
            if not doctor_doc:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            doctor_data = doctor_doc.to_dict()
            
            if not verify_password(password, doctor_data['password']):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = generate_jwt_token(doctor_data['uid'], email)
            doctor_data.pop('password')
            
            return Response({
                'message': 'Login successful',
                'doctor': doctor_data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from .auth import decode_jwt_token
            payload = decode_jwt_token(refresh_token)
            
            if payload.get('type') != 'refresh':
                return Response({'error': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
            
            tokens = generate_jwt_token(payload['uid'], payload['email'])
            
            return Response({
                'message': 'Token refreshed successfully',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorProfileView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, uid):
        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            doctor_data = doctor_doc.to_dict()
            doctor_data.pop('password', None)
            
            return Response(doctor_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, uid):
        serializer = DoctorProfileSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            update_data = {k: v for k, v in serializer.validated_data.items() 
                          if k not in ['uid', 'email', 'is_verified', 'created_at', 'password']}
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doctor_ref.update(update_data)
            
            updated_doc = doctor_ref.get()
            updated_data = updated_doc.to_dict()
            updated_data.pop('password', None)
            
            return Response({
                'message': 'Profile updated successfully',
                'doctor': updated_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class ToggleDoctorStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid):
        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            doctor_data = doctor_doc.to_dict()
            current_status = doctor_data.get('is_active', True)
            new_status = not current_status
            
            doctor_ref.update({
                'is_active': new_status,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            return Response({
                'message': f'Doctor status changed to {"active" if new_status else "inactive"}',
                'is_active': new_status
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            active_only = request.query_params.get('active_only', 'false').lower() == 'true'
            
            doctors_ref = db.collection('doctors')
            if active_only:
                docs = doctors_ref.where('is_active', '==', True).stream()
            else:
                docs = doctors_ref.stream()
            
            doctor_list = []
            for doc in docs:
                doctor_data = doc.to_dict()
                doctor_data.pop('password', None)
                doctor_list.append(doctor_data)
            
            return Response({
                'count': len(doctor_list),
                'doctors': doctor_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorAvailabilityView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, uid):
        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            doctor_data = doctor_doc.to_dict()
            availability = doctor_data.get('availability', [])
            
            return Response({
                'uid': uid,
                'availability': availability
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, uid):
        serializer = AvailabilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            availability_data = serializer.validated_data['availability']
            doctor_ref.update({
                'availability': availability_data,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            return Response({
                'message': 'Availability updated successfully',
                'availability': availability_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CheckDoctorAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid):
        day = request.query_params.get('day', '').lower()
        
        if not day:
            return Response({'error': 'Day parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day not in valid_days:
            return Response({
                'error': f'Invalid day. Must be one of: {", ".join(valid_days)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            doctor_data = doctor_doc.to_dict()
            
            if not doctor_data.get('is_active', True):
                return Response({
                    'uid': uid,
                    'day': day,
                    'is_available': False,
                    'message': 'Doctor is currently offline'
                }, status=status.HTTP_200_OK)
            
            availability = doctor_data.get('availability', [])
            day_availability = next((item for item in availability if item['day'] == day), None)
            
            if not day_availability:
                return Response({
                    'uid': uid,
                    'day': day,
                    'is_available': False,
                    'message': 'No availability set for this day'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'uid': uid,
                'day': day,
                'is_available': day_availability.get('is_available', False),
                'time_slots': day_availability.get('time_slots', [])
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class BookAppointmentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, doctor_uid):
        serializer = BookAppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            doctor_ref = db.collection('doctors').document(doctor_uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            doctor_data = doctor_doc.to_dict()
            
            if not doctor_data.get('is_active', True):
                return Response({
                    'error': 'Doctor is currently offline and not accepting appointments'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            availability = doctor_data.get('availability', [])
            
            day_index = None
            for i, day_avail in enumerate(availability):
                if day_avail['day'] == data['day']:
                    day_index = i
                    break
            
            if day_index is None:
                return Response({
                    'error': f'Doctor has no availability set for {data["day"]}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            time_slots = availability[day_index].get('time_slots', [])
            slot_index = None
            
            for i, slot in enumerate(time_slots):
                if slot['start_time'] == data['start_time'] and slot['end_time'] == data['end_time']:
                    slot_index = i
                    break
            
            if slot_index is None:
                return Response({'error': 'Requested time slot not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not time_slots[slot_index].get('is_available', True):
                return Response({'error': 'This time slot is already booked'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking_id = str(uuid.uuid4())
            
            availability[day_index]['time_slots'][slot_index]['is_available'] = False
            availability[day_index]['time_slots'][slot_index]['booked_by'] = data['patient_email']
            availability[day_index]['time_slots'][slot_index]['booking_id'] = booking_id
            
            doctor_ref.update({
                'availability': availability,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            appointment_data = {
                'booking_id': booking_id,
                'doctor_uid': doctor_uid,
                'doctor_name': f"{doctor_data['first_name']} {doctor_data['last_name']}",
                'patient_name': data['patient_name'],
                'patient_email': data['patient_email'],
                'patient_phone': data['patient_phone'],
                'day': data['day'],
                'start_time': data['start_time'],
                'end_time': data['end_time'],
                'reason': data.get('reason', ''),
                'status': 'confirmed',
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            db.collection('appointments').document(booking_id).set(appointment_data)
            
            return Response({
                'message': 'Appointment booked successfully',
                'booking_id': booking_id,
                'appointment': {
                    'booking_id': booking_id,
                    'doctor_name': appointment_data['doctor_name'],
                    'patient_name': data['patient_name'],
                    'day': data['day'],
                    'start_time': data['start_time'],
                    'end_time': data['end_time'],
                    'status': 'confirmed'
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CancelAppointmentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, booking_id):
        try:
            appointment_ref = db.collection('appointments').document(booking_id)
            appointment_doc = appointment_ref.get()
            
            if not appointment_doc.exists:
                return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
            appointment_data = appointment_doc.to_dict()
            
            doctor_ref = db.collection('doctors').document(appointment_data['doctor_uid'])
            doctor_doc = doctor_ref.get()
            
            if doctor_doc.exists:
                doctor_data = doctor_doc.to_dict()
                availability = doctor_data.get('availability', [])
                
                for day_avail in availability:
                    if day_avail['day'] == appointment_data['day']:
                        for slot in day_avail.get('time_slots', []):
                            if (slot.get('booking_id') == booking_id and
                                slot['start_time'] == appointment_data['start_time'] and
                                slot['end_time'] == appointment_data['end_time']):
                                slot['is_available'] = True
                                slot.pop('booked_by', None)
                                slot.pop('booking_id', None)
                                break
                
                doctor_ref.update({
                    'availability': availability,
                    'updated_at': firestore.SERVER_TIMESTAMP
                })
            
            appointment_ref.update({
                'status': 'cancelled',
                'cancelled_at': firestore.SERVER_TIMESTAMP
            })
            
            return Response({
                'message': 'Appointment cancelled successfully',
                'booking_id': booking_id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class ListAppointmentsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, doctor_uid):
        try:
            appointments_ref = db.collection('appointments')
            docs = appointments_ref.where('doctor_uid', '==', doctor_uid).stream()
            
            appointments = []
            for doc in docs:
                appointment_data = doc.to_dict()
                
                if 'patient_uid' in appointment_data:
                    patient_ref = db.collection('patients').document(appointment_data['patient_uid'])
                    patient_doc = patient_ref.get()
                    
                    if patient_doc.exists:
                        patient_data = patient_doc.to_dict()
                        appointment_data['patient_details'] = {
                            'uid': patient_data.get('uid'),
                            'name': f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}",
                            'email': patient_data.get('email'),
                            'phone_number': patient_data.get('phone_number'),
                            'date_of_birth': patient_data.get('date_of_birth'),
                            'address': patient_data.get('address'),
                            'emergency_contact': patient_data.get('emergency_contact')
                        }
                
                appointments.append(appointment_data)
            
            appointments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            return Response({
                'count': len(appointments),
                'appointments': appointments
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
