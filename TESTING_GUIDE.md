# Testing Guide - Doctor-Patient-Health Goals System

## Quick Start - Test Data Already Loaded!

You've already populated the database with test data. Here are the credentials:

### Test Credentials

**DOCTORS:**
- Email: `dr.smith@hospital.com` | Password: `Doctor123`
- Email: `dr.johnson@hospital.com` | Password: `Doctor123`
- Email: `dr.williams@hospital.com` | Password: `Doctor123`

**PATIENTS:**
- Email: `patient1@example.com` | Password: `Patient123`
- Email: `patient2@example.com` | Password: `Patient123`

---

## How to Check Doctor Availability

### Method 1: Through Frontend (Patient View)

1. **Login as Patient:**
   - Go to http://localhost:5174/patient-login
   - Email: `patient1@example.com`
   - Password: `Patient123`

2. **Book Appointment:**
   - Click "Book Appointment" button
   - Select a doctor from dropdown (Dr. Smith, Dr. Johnson, or Dr. Williams)
   - Select a day (Monday, Tuesday, Wednesday, Thursday, or Friday)
   - Available time slots will appear automatically
   - Select a time slot
   - Add reason (optional)
   - Click "Confirm"

3. **View Availability:**
   - When you select a doctor and day, the system automatically fetches available slots
   - Only available (green/unbooked) slots will be shown
   - Already booked slots won't appear in the list

### Method 2: Through API (Direct Testing)

**Check Doctor Availability API:**
```bash
# Get availability for a specific doctor on a specific day
curl -X GET "http://127.0.0.1:8000/api/doctors/check-availability/<doctor_uid>/?day=monday"
```

**Example:**
```bash
# First, get doctor list to find doctor_uid
curl http://127.0.0.1:8000/api/doctors/list/

# Then check availability (replace <doctor_uid> with actual UID)
curl "http://127.0.0.1:8000/api/doctors/check-availability/<doctor_uid>/?day=monday"
```

**Response will show:**
```json
{
  "doctor_name": "Dr. John Smith",
  "day": "monday",
  "time_slots": [
    {
      "start_time": "09:00",
      "end_time": "10:00",
      "is_available": true
    },
    {
      "start_time": "10:00",
      "end_time": "11:00",
      "is_available": false,
      "booked_by": "patient1@example.com"
    }
  ]
}
```

### Method 3: Check in Firestore Database

1. Go to Firebase Console
2. Navigate to Firestore Database
3. Open `doctors` collection
4. Select a doctor document
5. Look at the `availability` field
6. Each day has `time_slots` array showing which slots are available

---

## Testing All Features

### 1. Doctor Features

**Login as Doctor:**
```
URL: http://localhost:5174/doctor-login
Email: dr.smith@hospital.com
Password: Doctor123
```

**What to Test:**
- ✅ View appointments with patient details
- ✅ Toggle online/offline status
- ✅ Cancel appointments
- ✅ Logout

**Doctor Dashboard Shows:**
- Booking ID
- Patient name, email, phone
- Day and time of appointment
- Reason for visit
- Status (confirmed/cancelled)
- Cancel button for confirmed appointments

---

### 2. Patient Features

**Login as Patient:**
```
URL: http://localhost:5174/patient-login
Email: patient1@example.com
Password: Patient123
```

**What to Test:**
- ✅ View list of active doctors
- ✅ Check doctor availability by day
- ✅ Book appointments
- ✅ View own appointments
- ✅ Cancel appointments
- ✅ Navigate to Health Goals
- ✅ Logout

**Booking Flow:**
1. Click "Book Appointment"
2. Select doctor → See doctor's specialization
3. Select day → See available time slots
4. Select time slot → Confirm booking
5. Appointment appears in your list

---

### 3. Health Goals Features

**Access Health Goals:**
```
URL: http://localhost:5174/health-goals
(Must be logged in as patient)
```

**What to Test:**

**Daily Health Tracking:**
- Add daily metrics (steps, sleep, water, calories, exercise)
- View tracking history
- See recent 10 entries

**Medical Tests:**
- Add test records (name, date, result, doctor, notes)
- View all medical tests
- Track test history

**Preventive Checkups:**
- Add checkup records (type, date, doctor, findings, next date)
- View all checkups
- Track checkup schedule

---

## API Testing Guide

### Get All Doctors
```bash
curl http://127.0.0.1:8000/api/doctors/list/
```

### Get Active Doctors Only
```bash
curl http://127.0.0.1:8000/api/doctors/list/?active_only=true
```

### Check Doctor Availability
```bash
curl "http://127.0.0.1:8000/api/doctors/check-availability/<doctor_uid>/?day=monday"
```

### Get Doctor's Appointments
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://127.0.0.1:8000/api/doctors/appointments/<doctor_uid>/
```

### Get Patient's Appointments
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://127.0.0.1:8000/api/patients/appointments/<patient_uid>/
```

### Get Patient's Health Tracking
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://127.0.0.1:8000/api/health-goals/tracking/<patient_uid>/
```

---

## Current Availability Schedule

All doctors have the following availability:

**Monday:**
- 09:00 - 10:00
- 10:00 - 11:00
- 11:00 - 12:00
- 14:00 - 15:00
- 15:00 - 16:00

**Tuesday:**
- 09:00 - 10:00
- 10:00 - 11:00
- 14:00 - 15:00
- 15:00 - 16:00

**Wednesday:**
- 09:00 - 10:00
- 10:00 - 11:00
- 11:00 - 12:00

**Thursday:**
- 09:00 - 10:00
- 14:00 - 15:00
- 15:00 - 16:00

**Friday:**
- 09:00 - 10:00
- 10:00 - 11:00

---

## Troubleshooting

### Can't See Available Slots?
- Make sure doctor is online (is_active = true)
- Check that you selected a valid day (monday-friday)
- Verify doctor has availability set for that day

### Booking Fails?
- Check if slot is still available
- Verify you're logged in as patient
- Check browser console for error messages

### Can't See Appointments?
- Make sure you're logged in
- Check if you have any bookings
- Try refreshing the page (Ctrl+Shift+R)

### Health Goals Not Showing?
- Must be logged in as patient
- Check if data was populated (run populate_test_data.py)
- Verify patient_uid matches logged-in user

---

## Quick Test Checklist

- [ ] Doctor can login
- [ ] Doctor can see appointments
- [ ] Doctor can toggle online/offline
- [ ] Doctor can cancel appointments
- [ ] Patient can login
- [ ] Patient can see doctor list
- [ ] Patient can check availability
- [ ] Patient can book appointment
- [ ] Patient can view own appointments
- [ ] Patient can cancel appointment
- [ ] Patient can add health tracking
- [ ] Patient can add medical tests
- [ ] Patient can add preventive checkups
- [ ] Both can logout

---

## Need More Test Data?

Run the populate script again to add more doctors/patients:
```bash
cd c:\Users\Anirudh\temp\backend
python populate_test_data.py
```

Or manually register through the frontend:
- Doctor Register: http://localhost:5174/doctor-register
- Patient Register: http://localhost:5174/patient-register
