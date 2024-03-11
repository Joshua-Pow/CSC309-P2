from rest_framework import serializers
from .models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True, format="%Y-%m-%d")
    start_time = serializers.TimeField(required=True, format="%H:%M")
    end_time = serializers.TimeField(required=True, format="%H:%M")

    class Meta:
        model = TimeSlot
        fields = ["date", "start_time", "end_time"]

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError(
                {"time": "End time should be later than the start time."}
            )

        return data

    def create(self, validated_data):
        timeslot = TimeSlot.objects.create(
            date = validated_data["date"],
            start_time = validated_data["start_time"],
            end_time = validated_data["end_time"]
        )
        return timeslot
