"""
Populate Firestore database with temporary test data.
This creates sample doctors, patients, availability, and health goals.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
import uuid
from datetime import datetime, timedelta

# Initialize Firebase
cred_path = 'backend/serviceAccountKey.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_test_doctors():
    """Create 3 test doctors with availability"""
    doctors = [
        {
            'email': 'dr.smith@hospital.com',
            'password': 'Doctor123',
            'first_name': 'John',
            'last_name': 'Smith',
            'specialization': 'Cardiologist',
            'license_number': 'LIC001',
            'years_of_experience': 15,
            'phone_number': '555-0101',
            'bio': 'Experienced cardiologist specializing in heart disease prevention.'
        },
        {
            'email': 'dr.johnson@hospital.com',
            'password': 'Doctor123',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'specialization': 'Pediatrician',
            'license_number': 'LIC002',
            'years_of_experience': 10,
            'phone_number': '555-0102',
            'bio': 'Pediatrician with focus on child development and wellness.'
        },
        {
            'email': 'dr.williams@hospital.com',
            'password': 'Doctor123',
            'first_name': 'Michael',
            'last_name': 'Williams',
            'specialization': 'General Physician',
            'license_number': 'LIC003',
            'years_of_experience': 8,
            'phone_number': '555-0103',
            'bio': 'General physician providing comprehensive primary care.'
        }
    ]
    
    availability_schedule = [
        {
            "day": "monday",
            "is_available": True,
            "time_slots": [
                {"start_time": "09:00", "end_time": "10:00", "is_available": True},
                {"start_time": "10:00", "end_time": "11:00", "is_available": True},
                {"start_time": "11:00", "end_time": "12:00", "is_available": True},
                {"start_time": "14:00", "end_time": "15:00", "is_available": True},
                {"start_time": "15:00", "end_time": "16:00", "is_available": True},
            ]
        },
        {
            "day": "tuesday",
            "is_available": True,
            "time_slots": [
                {"start_time": "09:00", "end_time": "10:00", "is_available": True},
                {"start_time": "10:00", "end_time": "11:00", "is_available": True},
                {"start_time": "14:00", "end_time": "15:00", "is_available": True},
                {"start_time": "15:00", "end_time": "16:00", "is_available": True},
            ]
        },
        {
            "day": "wednesday",
            "is_available": True,
            "time_slots": [
                {"start_time": "09:00", "end_time": "10:00", "is_available": True},
                {"start_time": "10:00", "end_time": "11:00", "is_available": True},
                {"start_time": "11:00", "end_time": "12:00", "is_available": True},
            ]
        },
        {
            "day": "thursday",
            "is_available": True,
            "time_slots": [
                {"start_time": "09:00", "end_time": "10:00", "is_available": True},
                {"start_time": "14:00", "end_time": "15:00", "is_available": True},
                {"start_time": "15:00", "end_time": "16:00", "is_available": True},
            ]
        },
        {
            "day": "friday",
            "is_available": True,
            "time_slots": [
                {"start_time": "09:00", "end_time": "10:00", "is_available": True},
                {"start_time": "10:00", "end_time": "11:00", "is_available": True},
            ]
        }
    ]
    
    created_doctors = []
    for doctor in doctors:
        doctor_uid = str(uuid.uuid4())
        password = doctor.pop('password')
        
        doctor_data = {
            'uid': doctor_uid,
            **doctor,
            'password_hash': hash_password(password),
            'is_active': True,
            'availability': availability_schedule,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('doctors').document(doctor_uid).set(doctor_data)
        created_doctors.append({'uid': doctor_uid, 'email': doctor['email']})
        print(f"[OK] Created doctor: {doctor['first_name']} {doctor['last_name']} ({doctor['email']})")
    
    return created_doctors

def create_test_patients():
    """Create 2 test patients"""
    patients = [
        {
            'email': 'patient1@example.com',
            'password': 'Patient123',
            'first_name': 'Alice',
            'last_name': 'Brown',
            'phone_number': '555-0201',
            'date_of_birth': '1990-05-15',
            'address': '123 Main St, City, State 12345',
            'emergency_contact': '555-0999'
        },
        {
            'email': 'patient2@example.com',
            'password': 'Patient123',
            'first_name': 'Bob',
            'last_name': 'Davis',
            'phone_number': '555-0202',
            'date_of_birth': '1985-08-20',
            'address': '456 Oak Ave, City, State 12345',
            'emergency_contact': '555-0888'
        }
    ]
    
    created_patients = []
    for patient in patients:
        patient_uid = str(uuid.uuid4())
        password = patient.pop('password')
        
        patient_data = {
            'uid': patient_uid,
            **patient,
            'password_hash': hash_password(password),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('patients').document(patient_uid).set(patient_data)
        created_patients.append({'uid': patient_uid, 'email': patient['email']})
        print(f"[OK] Created patient: {patient['first_name']} {patient['last_name']} ({patient['email']})")
    
    return created_patients

def create_health_goals(patient_uid, patient_name):
    """Create sample health goals for a patient"""
    
    # Daily health tracking
    tracking_data = {
        'patient_uid': patient_uid,
        'date': '2025-12-19',
        'steps_taken': 8500,
        'hours_sleep': 7.5,
        'water_intake': 2.5,
        'calories_consumed': 2000,
        'exercise_minutes': 45,
        'notes': 'Feeling great today!',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('health_tracking').add(tracking_data)
    
    # Medical test
    test_data = {
        'patient_uid': patient_uid,
        'test_name': 'Complete Blood Count (CBC)',
        'test_date': '2025-12-15',
        'test_result': 'All values within normal range',
        'doctor_name': 'Dr. Smith',
        'notes': 'Annual health checkup',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('medical_tests').add(test_data)
    
    # Preventive checkup
    checkup_data = {
        'patient_uid': patient_uid,
        'checkup_type': 'Annual Physical Examination',
        'checkup_date': '2025-12-10',
        'doctor_name': 'Dr. Johnson',
        'findings': 'Overall health is excellent. Blood pressure and weight normal.',
        'next_checkup_date': '2026-12-10',
        'notes': 'Continue healthy lifestyle. Next checkup in 1 year.',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('preventive_checkups').add(checkup_data)
    
    print(f"[OK] Added health goals for: {patient_name}")

def main():
    print("=" * 70)
    print("POPULATING FIRESTORE WITH TEST DATA")
    print("=" * 70)
    print()
    
    # Create doctors
    print("Creating Test Doctors...")
    print("-" * 70)
    doctors = create_test_doctors()
    print()
    
    # Create patients
    print("Creating Test Patients...")
    print("-" * 70)
    patients = create_test_patients()
    print()
    
    # Add health goals for patients
    print("Adding Health Goals...")
    print("-" * 70)
    for patient in patients:
        # Get patient details
        patient_doc = db.collection('patients').document(patient['uid']).get()
        patient_data = patient_doc.to_dict()
        patient_name = f"{patient_data['first_name']} {patient_data['last_name']}"
        create_health_goals(patient['uid'], patient_name)
    print()
    
    print("=" * 70)
    print("[SUCCESS] DATABASE POPULATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("TEST CREDENTIALS:")
    print("-" * 70)
    print("\nDOCTORS:")
    print("   Email: dr.smith@hospital.com | Password: Doctor123")
    print("   Email: dr.johnson@hospital.com | Password: Doctor123")
    print("   Email: dr.williams@hospital.com | Password: Doctor123")
    print("\nPATIENTS:")
    print("   Email: patient1@example.com | Password: Patient123")
    print("   Email: patient2@example.com | Password: Patient123")
    print()
    print("All doctors have availability set for Mon-Fri")
    print("All patients have sample health tracking data")
    print()
    print("You can now login and test the application!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
