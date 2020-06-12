from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Schedule, ScheduleEntry
from rest_framework import status, viewsets, mixins
from ..serializers import ScheduleSerializer, ScheduleEntrySerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from datetime import datetime


class ScheduleEntryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ScheduleEntry.objects.order_by("shift_start_date")
    serializer_class = ScheduleEntrySerializer


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

    @action(detail=True, methods=["GET"])
    def list_entries(self, request: Request, pk: int):
        if (
            "from_date" not in request.query_params
            or "to_date" not in request.query_params
        ):
            return Response("Request query string missing from_date or to_date param.")

        from_date = datetime.fromisoformat(request.query_params["from_date"])
        to_date = datetime.fromisoformat(request.query_params["to_date"])
        delta = to_date - from_date
        weekly = delta.days > 7
        step = 7 if weekly else 1
        schedule = self.get_object()
        entries = schedule.scheduleentry_set.filter(
            shift_start_date__range=(from_date, to_date)
        )[::step]
        serializer = ScheduleEntrySerializer(entries, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=["POST"], url_path="entries",
    )
    def create_entries(self, request: Request, pk: int):
        if "entries" not in request.data:
            return Response("Missing 'entries' in request body")
        elif len(request.data["entries"]) == 0:
            return Response("Entries array cannot be empty")

        try:
            entries = []
            schedule = self.get_object()
            for entry in request.data["entries"]:
                schedule_entry = ScheduleEntry(
                    schedule=schedule,
                    author=schedule.team.teammember_set.get(pk=entry["author"]),
                    rotation=schedule.team.rotation_set.get(pk=entry["rotation"]),
                    team_member=schedule.team.teammember_set.get(
                        pk=entry["team_member"]
                    ),
                    shift_start_date=entry["shift_start_date"],
                    shift_end_date=entry["shift_end_date"],
                    is_backup=entry["is_backup"],
                    is_night=entry["is_night"],
                    is_off=entry["is_off"],
                    notes=entry["notes"],
                )
                entries.append(schedule_entry)
            ScheduleEntry.objects.bulk_create(entries)
            return Response(
                "Schedule entries created successfully", status=status.HTTP_201_CREATED
            )
        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST,)
        except ObjectDoesNotExist as err:
            return Response(str(err), status=status.HTTP_404_NOT_FOUND,)
        except Exception:
            return Response(
                "Unable to create entries. The error was related to: " + str(err),
                status=status.HTTP_400_BAD_REQUEST,
            )


# Create one/many -> POST api/v1/schedules/<int:id>/entries ✅
# list (date range) -> GET api/v1/schedules/<int:id>/entries?start=2020-06-10&end="2020-06-17" ✅
# Update one/many -> PUT/PATCH api/v1/schedules/<int:id>/entries
