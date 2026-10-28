from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id", "name", "specialization", "experience_years", "email",
            "phone", "created_by", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_experience_years(self, value):
        if value > 70:
            raise serializers.ValidationError("Enter a valid number of years.")
        return value

    
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be blank.")
        return value

    def validate_specialization(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Specialization cannot be blank.")
        return value
