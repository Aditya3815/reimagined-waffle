from rest_framework import serializers
import re

class DoctorRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    phone_number = serializers.CharField(required=False, max_length=15, allow_blank=True)
    specialization = serializers.CharField(required=False, max_length=100, allow_blank=True)
    license_number = serializers.CharField(required=False, max_length=50, allow_blank=True)
    years_of_experience = serializers.IntegerField(required=False, default=0, min_value=0)
    bio = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data


class DoctorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        return value.lower()


class TimeSlotSerializer(serializers.Serializer):
    start_time = serializers.CharField(max_length=5, help_text="Format: HH:MM (24-hour)")
    end_time = serializers.CharField(max_length=5, help_text="Format: HH:MM (24-hour)")
    is_available = serializers.BooleanField(default=True)
    booked_by = serializers.CharField(required=False, allow_blank=True, help_text="Patient UID if booked")
    booking_id = serializers.CharField(required=False, allow_blank=True, help_text="Unique booking ID")

    def validate_start_time(self, value):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise serializers.ValidationError("Invalid time format. Use HH:MM (24-hour)")
        return value

    def validate_end_time(self, value):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise serializers.ValidationError("Invalid time format. Use HH:MM (24-hour)")
        return value


class DayAvailabilitySerializer(serializers.Serializer):
    day = serializers.ChoiceField(
        choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    )
    is_available = serializers.BooleanField(default=True)
    time_slots = TimeSlotSerializer(many=True, required=False)


class AvailabilitySerializer(serializers.Serializer):
    availability = DayAvailabilitySerializer(many=True)

    def validate_availability(self, value):
        days = [item['day'] for item in value]
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Duplicate days found in availability")
        return value


class DoctorProfileSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    specialization = serializers.CharField(max_length=100, required=False, allow_blank=True)
    license_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    years_of_experience = serializers.IntegerField(required=False, default=0, min_value=0)
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.URLField(required=False, allow_blank=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(required=False, help_text="Doctor's online/offline status")
    availability = DayAvailabilitySerializer(many=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BookAppointmentSerializer(serializers.Serializer):
    patient_name = serializers.CharField(max_length=100)
    patient_email = serializers.EmailField()
    patient_phone = serializers.CharField(max_length=15)
    day = serializers.ChoiceField(
        choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    )
    start_time = serializers.CharField(max_length=5)
    end_time = serializers.CharField(max_length=5)
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_start_time(self, value):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise serializers.ValidationError("Invalid time format. Use HH:MM (24-hour)")
        return value

    def validate_end_time(self, value):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise serializers.ValidationError("Invalid time format. Use HH:MM (24-hour)")
        return value
