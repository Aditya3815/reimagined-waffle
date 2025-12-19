"""
Check if doctors have availability data in Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred_path = 'backend/serviceAccountKey.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_availability():
    print("=" * 70)
    print("CHECKING DOCTOR AVAILABILITY IN DATABASE")
    print("=" * 70)
    print()
    
    # Get all doctors
    doctors_ref = db.collection('doctors')
    doctors = doctors_ref.stream()
    
    doctor_count = 0
    for doc in doctors:
        doctor_count += 1
        doctor_data = doc.to_dict()
        
        print(f"Doctor: {doctor_data.get('first_name')} {doctor_data.get('last_name')}")
        print(f"Email: {doctor_data.get('email')}")
        print(f"UID: {doc.id}")
        print(f"Is Active: {doctor_data.get('is_active', False)}")
        
        # Check if availability exists
        availability = doctor_data.get('availability', [])
        
        if not availability:
            print("[ERROR] NO AVAILABILITY DATA FOUND!")
        else:
            print(f"[OK] Has availability for {len(availability)} days:")
            for day_avail in availability:
                day = day_avail.get('day')
                slots = day_avail.get('time_slots', [])
                available_count = sum(1 for slot in slots if slot.get('is_available', False))
                print(f"  - {day.capitalize()}: {len(slots)} total slots, {available_count} available")
        
        print("-" * 70)
        print()
    
    if doctor_count == 0:
        print("[ERROR] NO DOCTORS FOUND IN DATABASE!")
        print("Run: python populate_test_data.py")
    else:
        print(f"Total doctors checked: {doctor_count}")
    
    print("=" * 70)

if __name__ == "__main__":
    check_availability()
