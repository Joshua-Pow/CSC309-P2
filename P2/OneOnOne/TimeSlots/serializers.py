from rest_framework import serializers
from .models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(required=True, format="%H:%M")
    end_time = serializers.TimeField(required=True, format="%H:%M")

    class Meta:
        model = TimeSlot
        fields = ["id", "start_time", "end_time"]
        extra_kwargs = {"day": {"write_only": True, "required": False}}

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError(
                {"time": "End time should be later than the start time."}
            )

        return data

    def create(self, validated_data):
        timeslot = TimeSlot.objects.create(**validated_data)
        return timeslot
