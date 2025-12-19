"""
Script to add doctor availability and health goals data to Firestore database.
Run this after registering doctors and patients.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# Initialize Firebase - serviceAccountKey.json is in backend/backend/ folder
cred_path = os.path.join(os.path.dirname(__file__), 'backend', 'serviceAccountKey.json')
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def add_doctor_availability(doctor_email):
    """
    Add availability schedule for a doctor.
    """
    # Find doctor by email
    doctors_ref = db.collection('doctors')
    docs = doctors_ref.where('email', '==', doctor_email).limit(1).stream()
    
    doctor_doc = None
    for doc in docs:
        doctor_doc = doc
        break
    
    if not doctor_doc:
        print(f"Doctor with email {doctor_email} not found!")
        return
    
    doctor_uid = doctor_doc.id
    
    # Sample availability schedule
    availability = [
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
    
    # Update doctor's availability
    doctors_ref.document(doctor_uid).update({
        'availability': availability,
        'updated_at': firestore.SERVER_TIMESTAMP
    })
    
    print(f"Added availability for doctor: {doctor_email}")
    print(f"   - Monday: 5 slots")
    print(f"   - Tuesday: 3 slots")
    print(f"   - Wednesday: 3 slots")
    print(f"   - Thursday: 3 slots")
    print(f"   - Friday: 2 slots")


def add_patient_health_goals(patient_email):
    """
    Add sample health goals data for a patient.
    """
    # Find patient by email
    patients_ref = db.collection('patients')
    docs = patients_ref.where('email', '==', patient_email).limit(1).stream()
    
    patient_doc = None
    for doc in docs:
        patient_doc = doc
        break
    
    if not patient_doc:
        print(f"Patient with email {patient_email} not found!")
        return
    
    patient_uid = patient_doc.id
    
    # Add daily health tracking
    health_tracking_data = {
        'patient_uid': patient_uid,
        'date': '2025-12-19',
        'steps_taken': 8500,
        'hours_sleep': 7.5,
        'water_intake': 2.5,
        'calories_consumed': 2000,
        'exercise_minutes': 45,
        'notes': 'Feeling energetic today!',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    db.collection('health_tracking').add(health_tracking_data)
    print(f"Added health tracking for patient: {patient_email}")
    
    # Add medical test
    medical_test_data = {
        'patient_uid': patient_uid,
        'test_name': 'Blood Test - Complete Blood Count',
        'test_date': '2025-12-15',
        'test_result': 'Normal - All values within range',
        'doctor_name': 'Dr. Smith',
        'notes': 'Annual checkup',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    db.collection('medical_tests').add(medical_test_data)
    print(f"Added medical test for patient: {patient_email}")
    
    # Add preventive checkup
    preventive_checkup_data = {
        'patient_uid': patient_uid,
        'checkup_type': 'Annual Physical Examination',
        'checkup_date': '2025-12-10',
        'doctor_name': 'Dr. Johnson',
        'findings': 'Overall health is good. Blood pressure normal. Weight stable.',
        'next_checkup_date': '2026-12-10',
        'notes': 'Continue current lifestyle. Schedule next checkup in 1 year.',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    db.collection('preventive_checkups').add(preventive_checkup_data)
    print(f"Added preventive checkup for patient: {patient_email}")


def main():
    print("=" * 60)
    print("FIRESTORE DATA POPULATION SCRIPT")
    print("=" * 60)
    print()
    
    # Example usage - Replace with your actual emails
    print("Adding Doctor Availability...")
    print("-" * 60)
    
    # Add availability for doctors (replace with actual doctor emails)
    doctor_emails = [
        "doctor1@example.com",  # Replace with your doctor's email
        # Add more doctor emails here
    ]
    
    for email in doctor_emails:
        try:
            add_doctor_availability(email)
            print()
        except Exception as e:
            print(f" Error adding availability for {email}: {str(e)}")
            print()
    
    print("Adding Patient Health Goals...")
    print("-" * 60)
    
    # Add health goals for patients (replace with actual patient emails)
    patient_emails = [
        "patient1@example.com",  # Replace with your patient's email
        # Add more patient emails here
    ]
    
    for email in patient_emails:
        try:
            add_patient_health_goals(email)
            print()
        except Exception as e:
            print(f"Error adding health goals for {email}: {str(e)}")
            print()
    
    print("=" * 60)
    print("DATA POPULATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    print()
    print(" INSTRUCTIONS:")
    print("1. First register doctors and patients through the frontend")
    print("2. Update the email lists in this script with actual emails")
    print("3. Run: python add_availability_and_goals.py")
    print()
    
    response = input("Have you updated the email lists? (yes/no): ")
    if response.lower() == 'yes':
        main()
    else:
        print("\n Please update the email lists in the script first!")
        print("   Edit lines 188 and 200 with your actual doctor/patient emails.")
