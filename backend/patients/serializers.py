from rest_framework import serializers
import re

class PatientRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    phone_number = serializers.CharField(required=False, max_length=15, allow_blank=True)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(required=False, max_length=15, allow_blank=True)

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data


class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        return value.lower()


class PatientProfileSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(max_length=15, required=False, allow_blank=True)
    profile_picture = serializers.URLField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BookAppointmentSerializer(serializers.Serializer):
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
