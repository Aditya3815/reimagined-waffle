from rest_framework import serializers

class HealthGoalSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Date of tracking (YYYY-MM-DD)")
    steps_taken = serializers.IntegerField(min_value=0, required=False, help_text="Number of steps taken")
    hours_sleep = serializers.FloatField(min_value=0, max_value=24, required=False, help_text="Hours of sleep")
    water_intake = serializers.FloatField(min_value=0, required=False, help_text="Water intake in liters")
    calories_consumed = serializers.IntegerField(min_value=0, required=False, help_text="Calories consumed")
    exercise_minutes = serializers.IntegerField(min_value=0, required=False, help_text="Exercise duration in minutes")
    notes = serializers.CharField(required=False, allow_blank=True, help_text="Additional notes")


class MedicalTestSerializer(serializers.Serializer):
    test_name = serializers.CharField(max_length=200)
    test_date = serializers.DateField()
    test_result = serializers.CharField(required=False, allow_blank=True)
    doctor_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    file_url = serializers.URLField(required=False, allow_blank=True, help_text="URL to test report")


class PreventiveCheckupSerializer(serializers.Serializer):
    checkup_type = serializers.CharField(max_length=200, help_text="Type of checkup (e.g., Annual Physical, Dental)")
    checkup_date = serializers.DateField()
    doctor_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    findings = serializers.CharField(required=False, allow_blank=True)
    next_checkup_date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)


class HealthGoalSummarySerializer(serializers.Serializer):
    patient_uid = serializers.CharField(read_only=True)
    patient_name = serializers.CharField(read_only=True)
    total_days_tracked = serializers.IntegerField(read_only=True)
    avg_steps = serializers.FloatField(read_only=True)
    avg_sleep = serializers.FloatField(read_only=True)
    total_tests = serializers.IntegerField(read_only=True)
    total_checkups = serializers.IntegerField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
