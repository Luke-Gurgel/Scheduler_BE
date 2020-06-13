from rest_framework import viewsets, mixins
from ..models import Schedule, ScheduleEntry
from ..serializers import ScheduleSerializer, ScheduleEntrySerializer


class ScheduleViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    """A viewset for creating, retrieving and listing schedules."""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
