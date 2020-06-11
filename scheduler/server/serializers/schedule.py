from rest_framework import serializers
from ..models import Schedule, ScheduleEntry, ScheduleChangeRequest


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEntry
        fields = "__all__"


class ScheduleChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangeRequest
        fields = "__all__"
