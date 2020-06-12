from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import ScheduleSerializer
from rest_framework import status, viewsets, mixins
from ..models import Schedule


class ScheduleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """A viewset for creating, retrieving and listting schedules."""

    queryset = Schedule.objects.order_by("-start_date")
    serializer_class = ScheduleSerializer
