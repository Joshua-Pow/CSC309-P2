from rest_framework import serializers
from .models import Calendar, Day


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ["id", "date", "ranking"]


class CalendarSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True)

    def create(self, validated_data):
        days_data = validated_data.pop("days")
        calendar = Calendar.objects.create(**validated_data)
        for day_data in days_data:
            Day.objects.create(calendar=calendar, **day_data)
        return calendar

    def validate_days(self, value):
        if not value:
            raise serializers.ValidationError(
                "Days field must include at least one day with date and ranking."
            )
        for day in value:
            if "date" not in day or "ranking" not in day:
                raise serializers.ValidationError(
                    "Each day must include both 'date' and 'ranking' keys."
                )
        return value

    def update(self, instance, validated_data):
        days_data = validated_data.pop("days", None)
        if days_data is not None:
            instance.days.all().delete()  # Remove existing days
            for day_data in days_data:
                Day.objects.create(calendar=instance, **day_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Calendar
        fields = ["id", "title", "description", "days"]
