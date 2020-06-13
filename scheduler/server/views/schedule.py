from rest_framework import viewsets, mixins
from ..models import Schedule, ScheduleEntry
from ..serializers import ScheduleSerializer, ScheduleEntrySerializer


class ScheduleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """A viewset for creating, retrieving and listing schedules."""

    queryset = Schedule.objects.order_by("-start_date")
    serializer_class = ScheduleSerializer
